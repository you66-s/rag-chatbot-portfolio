from typing import List

from schemas.response.RetrievedDocuments import RetrievedDocumentsResponse

class PromptBuilder:
    def __init__(self, documents: List[RetrievedDocumentsResponse]):
        self.documents = documents