from enum import Enum

class EmbeddingParameters(Enum):
    EMBEDDING_RETRIEVAL_DOCUMENT_TASK = "RETRIEVAL_DOCUMENT"
    EMBEDDING_QUESTION_TASK = "QUESTION_ANSWERING"


class LLMProcessingResponses(Enum):
    LLM_CLIENT_NOT_INITIALIZED = "llm model not initialized."
    LLM_TEXT_GENERATION_ERROR = "Error While generating text, please try later"
    LLM_TEXT_EMBEDDING_FAIL = "Error while generating embedding, please try later"
    
class VectorDBResponses(Enum):
    COLLECTION_CREATION_SUCCESS = "Collection has been created successfully"
    COLLECTION_CREATION_FAILED = "Collection not created"
    COLLECTION_NOT_EXISTS = "Collection name not exists"
    DOCUMENT_INSERTION_SUCCESS = "Document has been successfully inserted"
    DOCUMENT_INSERTION_FAILED = "Failed to insert document, please try later"