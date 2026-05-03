from typing import List
from langchain_core.documents import Document
from qdrant_client.models import PointStruct
from enums.LLMEnums import EmbeddingParameters
from store.llm.PromptBuilder import PromptBuilder
import logging

class NLPController:
    def __init__(self, vectord_db, llm):
        self.vectord_db = vectord_db
        self.llm = llm
        self.logger = logging.getLogger(__name__)
    
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
    
    def prepare_prompt(self, query: str, collection_name: str) -> str:
        """
        This function builds full prompt and prepare it for using by llm
        """
        
        retrieved_documents, retrieve_msg = self.retrieve_similaire_documents(query=query, collection_name=collection_name)
        if retrieved_documents is None or len(retrieved_documents) == 0:
            return None, retrieve_msg
        try:
            prompt = PromptBuilder(documents=retrieved_documents, query=query).build_prompt()
            print("1- NLPController: Prompt builded...")
            return prompt, None
        except Exception as e:
            self.logger.error(f"Prompt Builder Error: {type(e).__name__} - {str(e)}")
            return None, "Error while building the prompt"

        
    def clear_chat_history(self):
        self.llm.clear_chat_session()
        
    def list_chat_history(self):
        print("4- NLPController: Listing chat history...")
        history, msg = self.llm.list_chat_history()
        if history is None:
            return None, msg
        formatted_history = [
            {
                "role": message.role,
                "text": message.parts[0].text
            }
            for message in history
        ]
        return formatted_history, None