from typing import List
from schemas.request.CollectionSchema import CreateCollectionSchema
from langchain_core.documents import Document
from qdrant_client.models import PointStruct
from enums.LLMEnums import EmbeddingParameters

class NLPController:
    def __init__(self, vectord_db, llm):
        self.vectord_db = vectord_db
        self.llm = llm
    
    def get_collection_info(self, collection_name: str):
        collection_info = self.vectord_db.get_collection_info(collection_name=collection_name)
        return collection_info
    
    def index_chunk(self, collection_name: str, id: int, chunk: Document, payload: dict):
        point = PointStruct(
            id=id,
            vector=self.llm.embed_text(text=chunk.page_content, task_type=EmbeddingParameters.EMBEDDING_RETRIEVAL_DOCUMENT_TASK.value),
            payload=payload
        )
        is_inserted, message = self.vectord_db.insert_document(collection_name=collection_name, point=point)
        return is_inserted, message
    
    def retrieve_similaire_documents(self, query: str, collection_name: str):
        """
        This function retrieve similaire documents (chunks) to user's query and feeded into llm answer template
        """
        vector = self.llm.embed_text(text=query, task_type=EmbeddingParameters.EMBEDDING_QUESTION_TASK.value)
        if vector is None or len(vector) == 0:
            return None,  "Error while embedding text"
        
        search_result, search_msg = self.vectord_db.search(vector=vector, collection_name=collection_name)
        return search_result, search_msg
    
    def prepare_rag_answer(self, query: str, collection_name: str):
        retrieved_documents, retrieve_msg = self.retrieve_similaire_documents(query=query, collection_name=collection_name)
        if retrieved_documents is None or len(retrieved_documents) == 0:
            return None, retrieve_msg
        system_prompt = """
        
        
        
        """
        
        