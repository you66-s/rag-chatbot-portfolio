from pydantic import BaseModel

class CreateCollectionSchema(BaseModel):
    """
    This schema define how the user will creates it schemes in his account
    Each schema is defined by a name, description, Resume Section (Education, skills...)
    """
    
    name: str
    embedding_size: int
    payload: dict