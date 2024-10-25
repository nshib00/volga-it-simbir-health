from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import sys
from pathlib import Path
from elasticsearch import AsyncElasticsearch

from document.app.service import HistoryService


path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from document.app.api import router as document_router
from document.app.config import settings
from document.elastic.service import ElasticService


elastic_client = AsyncElasticsearch(
    hosts=settings.ELASTIC_URL,
    basic_auth=(settings.ELASTIC_USER, settings.ELASTIC_PASSWORD)
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ElasticService.create_index_if_not_exists(elastic_client)
    history_data: list[dict] = await HistoryService.get_history_data_to_sync()
    # if not history_data:
    await ElasticService.fill_index(history_data, elastic_client)
    yield
    await elastic_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(document_router)
app.state.elastic_client = elastic_client


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SimbirHealth | Document API",
        version="1.0.0",
        summary="Работа с документами",
        description="Документация API микросервиса документов SimbirHealth.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8084, reload=True)