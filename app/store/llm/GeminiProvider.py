from core.config import get_settings
from google import genai
from google.genai import types
from enums.LLMEnums import LLMProcessingResponses
import numpy as np
import logging

class GeminiProvider():
    def __init__(self, temperature: float=0.1, max_output_tokens: int=1000, max_input_token: int = 2048):
        self.__settings = get_settings()
        self.logger = logging.getLogger(__name__)
        self.embedding_model_id = self.__settings.EMBEDDING_MODEL_ID
        self.embedding_size = self.__settings.EMBEDDING_OUTPUT_VECTOR_SIZE
        self.generation_model_id = self.__settings.GENERATION_MODEL_ID
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.max_input_token = max_input_token
        self.__client =genai.Client(api_key=self.__settings.GEMINI_MODEL_API_KEY)
        self.chat = self.initialize_chat_session()
        
    def initialize_chat_session(self):
        """
        This function is used to initialize a chat session
        """
        chat = self.__client.chats.create(
            model=self.generation_model_id,
            config=types.GenerateContentConfig(
                system_instruction="You are a professional AI assistant representing Youssef Achehboune, an ML/AI Engineer. Your name is Joseph",
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens
            )
        )
        return chat
    
    def clear_chat_session(self):
        """
        this function used to clean chat history after user end chat and start a new one.
        """
        self.chat = self.initialize_chat_session()
        
    def clean_text(self, text: str):
        return text[:self.max_input_token].strip()
        
    def generate_response(self, prompt: str):
        """
        This function is the responsible on the text generation based on user's prompt
        """
        if not self.__client or not self.generation_model_id:
            self.logger.error(f"Client Error: {self.__client} | {self.embedding_model_id} | {self.generation_model_id}")
            return None, LLMProcessingResponses.LLM_CLIENT_NOT_INITIALIZED.value
        
        try:
            response = self.chat.send_message(message=prompt)
            print("2- Genimi provider: response generation...")
            return response.text, None
        except Exception as e:
            self.logger.error(f"Text generation error: {type(e).__name__} - {str(e)}")
            return None, LLMProcessingResponses.LLM_TEXT_GENERATION_ERROR.value

    
    
    def embed_text(self, text: str, task_type: str = None):
        if not self.__client or not self.embedding_model_id:
            self.logger.error(f"Client Error: {self.__client} | {self.embedding_model_id} | {self.generation_model_id}")
            return None, LLMProcessingResponses.LLM_CLIENT_NOT_INITIALIZED.value
        try:
            response = self.__client.models.embed_content(
                model=self.__settings.EMBEDDING_MODEL_ID,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=self.embedding_size
                )
            )
            embedding = response.embeddings[0].values   # this variable contains raw embeddings
            if self.embedding_size != 3072:
                normalized_embd = embedding / np.linalg.norm(embedding)  #  must manually normalize non-3072 dimensions
                return normalized_embd   
            return embedding
        except Exception as e:
            self.logger.error(f"Text embedding error: {type(e).__name__} - {str(e)}")
            return None