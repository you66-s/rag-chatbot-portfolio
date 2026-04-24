from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    file_id: str = None
    path: str = None
    message: str