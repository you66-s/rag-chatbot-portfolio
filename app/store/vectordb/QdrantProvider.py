import logging
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from schemas.request.CollectionSchema import CreateCollectionSchema
from enums.LLMEnums import VectorDBResponses
from schemas.response.RetrievedDocuments import RetrievedDocumentsResponse
class QdrantProvider:
    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")
        self.distance = Distance.COSINE
        self.logger = logging.getLogger(__name__)
        
    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        
    def create_collection(self, collection: CreateCollectionSchema):
        try:
            if not self.is_collection_existed(collection_name=collection.name):
                _ = self.client.create_collection(
                    collection_name=collection.name,
                    vectors_config=VectorParams(
                        size=collection.embedding_size,
                        distance=self.distance
                    )
                )
                return True, VectorDBResponses.COLLECTION_CREATION_SUCCESS.value
        except Exception as e:
            self.logger.error(f"Collection creation error: {type(e).__name__} - {str(e)}")
            return False, VectorDBResponses.COLLECTION_CREATION_FAILED.value
        
    def insert_document(self, collection_name: str, point: PointStruct):
        """
        this function takes 1 point and insert it into a given collection
        """
        
        if not self.is_collection_existed(collection_name=collection_name):
            return False, VectorDBResponses.COLLECTION_NOT_EXISTS.value
        try:
            _ = self.client.upsert(
                collection_name=collection_name,
                points=[point],
            )
            return True, VectorDBResponses.DOCUMENT_INSERTION_SUCCESS.value
        except Exception as e:
            self.logger.error(f"Document insertion error: {type(e).__name__} - {str(e)}")
            return False, VectorDBResponses.DOCUMENT_INSERTION_FAILED.value
        
    def search(self, vector: list, collection_name: str, top_k: int = 5) -> List[RetrievedDocumentsResponse]:
        """
        This function take a vector and a collection name and perform a similarity search between user's vector query and the documents's vectors stored in that given collection name and return a list of retrieved document schema
        """
        try:
            search_result = self.client.query_points(
                collection_name=collection_name,
                query=vector,
                limit=top_k,
                with_payload=True,
                score_threshold=0.6
            )
            if search_result is None or len(search_result.points) == 0:
                return None, "0 Document retrieved."
            return [
                RetrievedDocumentsResponse(**{
                    "text": result.payload["text"],
                    "section": result.payload["section"],
                    "score": result.score,
                    "description": result.payload["description"]
                })
                for result in search_result.points
            ], None
        except Exception as e:
            self.logger.error(f"query search error: {type(e).__name__} - {str(e)}")
            return None, "Error while searching for user's query"