from datetime import datetime
from elasticsearch import AsyncElasticsearch
from sqlalchemy import ScalarResult

from document.dto import HistoryDTO
from document.elastic.mappings import ELASTIC_MAPPINGS
from document.elastic.query import get_documents_query


class ElasticService:
    index_name = 'documents'

    @classmethod
    async def add_document(cls, elastic_client: AsyncElasticsearch, data: ScalarResult) -> None:
        document = HistoryDTO.to_dict(history_obj=data)
        await elastic_client.index(id=data.id, document=document, index=cls.index_name)

    @classmethod
    async def update_document(cls, elastic_client: AsyncElasticsearch, data: ScalarResult) -> None:
        document = HistoryDTO.to_dict(history_obj=data)
        await elastic_client.update(index=cls.index_name, id=str(data.id), doc=document)

    @classmethod
    async def create_index_if_not_exists(cls, elastic_client: AsyncElasticsearch) -> None:
        await elastic_client.indices.delete(index=cls.index_name)
        if not (await elastic_client.indices.exists(index=cls.index_name)):
            await elastic_client.indices.create(index=cls.index_name, mappings=ELASTIC_MAPPINGS)

    @classmethod
    async def fill_index(cls, data, elastic_client: AsyncElasticsearch) -> None:
        for doc_id, doc in enumerate(data, start=1):
            await elastic_client.index(id=doc_id, document=doc, index=cls.index_name)

    @classmethod
    async def search_in_history(
        cls,
        user_query: str,
        elastic_client: AsyncElasticsearch,
        pacient_id: int | None = None,
        date: datetime | None = None,
        hospital_id: int | None = None,
        doctor_id: int | None = None,
    ):
        documents_query = get_documents_query(
            query=user_query,
            pacient_id=pacient_id,
            hospital_id=hospital_id,
            doctor_id=doctor_id,
            history_date=date
        )
        search_result = await elastic_client.search(
            index=cls.index_name,
            query=documents_query,
            filter_path='hits.hits._id,hits.hits._score,hits.hits._source'
        )
        return search_result


    

        



