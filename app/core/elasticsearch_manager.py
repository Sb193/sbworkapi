from elasticsearch import AsyncElasticsearch
from app.core.config import settings
from typing import Dict, Any, Optional
import json

class ElasticsearchManager:
    def __init__(self):
        self.es = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
        self.indices = {
            "jobs": {
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "text", "analyzer": "vi_analyzer"},
                        "description": {"type": "text", "analyzer": "vi_analyzer"},
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
                },
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "vi_analyzer": {
                                "tokenizer": "vi_tokenizer"
                            }
                        }
                    }
                }
            },
            "recruiters": {
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "vi_analyzer"},
                        "description": {"type": "text", "analyzer": "vi_analyzer"},
                        "location": {"type": "text", "analyzer": "vi_analyzer"},
                        "company_size": {"type": "keyword"},
                        "industry": {"type": "keyword"},
                        "created_at": {"type": "date"}
                    }
                },
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "vi_analyzer": {
                                "tokenizer": "vi_tokenizer"
                            }
                        }
                    }
                }
            },
            "users": {
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "keyword"},
                        "email": {"type": "keyword"},
                        "full_name": {"type": "text", "analyzer": "vi_analyzer"},
                        "location": {"type": "text", "analyzer": "vi_analyzer"},
                        "skills": {"type": "keyword"},
                        "experience": {"type": "text", "analyzer": "vi_analyzer"},
                        "created_at": {"type": "date"}
                    }
                },
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "vi_analyzer": {
                                "tokenizer": "vi_tokenizer"
                            }
                        }
                    }
                }
            }
        }

    async def init_indices(self):
        """Khởi tạo tất cả các index"""
        for index_name, index_config in self.indices.items():
            if not await self.es.indices.exists(index=index_name):
                await self.es.indices.create(
                    index=index_name,
                    body=index_config
                )

    async def index_document(self, index_name: str, document_id: int, document: Dict[str, Any]):
        """Index một document vào Elasticsearch"""
        await self.es.index(
            index=index_name,
            id=document_id,
            document=document
        )

    async def delete_document(self, index_name: str, document_id: int):
        """Xóa một document khỏi Elasticsearch"""
        await self.es.delete(
            index=index_name,
            id=document_id
        )

    async def search(self, index_name: str, query: Dict[str, Any], 
                    from_: int = 0, size: int = 10, 
                    sort: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Tìm kiếm trong Elasticsearch"""
        body = {
            "query": query,
            "from": from_,
            "size": size
        }
        if sort:
            body["sort"] = sort

        return await self.es.search(
            index=index_name,
            body=body
        )

    async def close(self):
        """Đóng kết nối Elasticsearch"""
        await self.es.close()

# Tạo instance global
es_manager = ElasticsearchManager() 