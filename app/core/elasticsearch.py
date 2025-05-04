from elasticsearch import AsyncElasticsearch
from app.core.config import settings

es = AsyncElasticsearch(
    hosts=[f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"],
    verify_certs=False,
    timeout=30,
    max_retries=3,
    retry_on_timeout=True
)

async def init_elasticsearch():
    # Create index if not exists
    if not await es.indices.exists(index="jobs"):
        await es.indices.create(
            index="jobs",
            body={
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "text", "analyzer": "standard"},
                        "description": {"type": "text", "analyzer": "standard"},
                        "salary_min": {"type": "integer"},
                        "salary_max": {"type": "integer"},
                        "location_id": {"type": "integer"},
                        "work_type_id": {"type": "integer"},
                        "recruiter_id": {"type": "integer"},
                        "experience_level": {"type": "keyword"},
                        "industry": {"type": "keyword"},
                        "created_at": {"type": "date"},
                        "tags": {"type": "keyword"}
                    }
                }
            }
        )

async def close_elasticsearch():
    await es.close() 