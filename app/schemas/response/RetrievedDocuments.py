from pydantic import BaseModel

class RetrievedDocumentsResponse(BaseModel):
    text: str
    section: str
    score: float
    description: str