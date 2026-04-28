from fastapi import APIRouter, Request, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from controllers.FileController import FileController
from schemas.response.fileSchema import FileUploadResponse
file_route = APIRouter(prefix="/api/v1/data", tags=["Data"])
file_controller = FileController()

@file_route.post("/upload-file", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    is_valid, validation_message = file_controller.validate_file(file=file)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation_message
        )
    is_stored, response = await file_controller.store_uploaded_file(file=file)
    if not is_stored:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response
        )
    return response
