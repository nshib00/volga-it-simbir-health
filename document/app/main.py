import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(path))

from document.app.api import router as document_router


app = FastAPI()
app.include_router(document_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8084, reload=True)