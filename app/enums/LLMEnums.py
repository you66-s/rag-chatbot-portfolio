from enum import Enum

class LLMParameters(Enum):
    EMBEDDING_RETRIEVAL_DOCUMENT_TASK = "RETRIEVAL_DOCUMENT"
    EMBEDDING_QUESTION_TASK = "QUESTION_ANSWERING"

class LLMProcessingResponses(Enum):
    LLM_CLIENT_NOT_INITIALIZED = "llm model not initialized."
    LLM_TEXT_GENERATION_ERROR = "Error While generating text, please try later"
    LLM_TEXT_EMBEDDING_FAIL = "Error while generating embedding, please try later"