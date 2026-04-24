from fastapi import UploadFile, File
from core.config import get_settings
from enums.FileEnums import FileProcessingResponses
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import aiofiles, uuid, logging, os

class FileController:
    def __init__(self):
        self.__settings = get_settings()
        self.__STORING_PATH = Path("storage")     # Dev attributes
        self.logger = logging.getLogger(__name__)
    def validate_file(self, file: UploadFile = File(...)) -> bool:
        if file.content_type != self.__settings.FILE_ALLOWED_TYPES:
            return False, FileProcessingResponses.FILE_FORMAT_NOT_VALIDE.value
        if file.size > self.__settings.FILE_MAX_SIZE:
            return False, FileProcessingResponses.FILE_SIZE_EXCEEDED.value
        return True, FileProcessingResponses.FILE_UPLOAD_SUCCESS.value
    
    # Dev functions
    async def store_uploaded_file(self, file: UploadFile = File(...)):
        file_id = uuid.uuid4()
        dst = self.__STORING_PATH / f"{str(file_id)}"   # full path of file in storage
        try:
            os.makedirs(dst, exist_ok=False)
            file_path = os.path.join(dst, file.filename)
            async with aiofiles.open(file_path, "wb") as out:
                while chunk := await file.read(1024 * 1024):
                    await out.write(chunk)
            return True, {
                "file_id": str(file_id),
                "path": file_path,
                "message": FileProcessingResponses.FILE_STORAGE_SUCCESS.value
            }
        except Exception as e:
            self.logger.error(f"Error while storing file: {e}")
            return False, {
                "file_id": str(file_id),
                "path": file_path,
                "message": FileProcessingResponses.FILE_STORAGE_FAIL.value
            }
            
            
    def file_content_loading(self, file_id: str) -> List[Document]:
        """
        This function load the file content only and clean it us langchain and PyMuPDFLoader if needed
        Returns list of Documents
        """
        file_path = os.path.join(self.__STORING_PATH, file_id, os.listdir(os.path.join(self.__STORING_PATH, file_id))[0])    # file path
        if file_path is None:
            return None, FileProcessingResponses.FILE_SEARCH_BY_ID_NOT_FOUND.value
        try:
            loader = PyMuPDFLoader(file_path=file_path)
            documents = loader.load()
            return documents, None
        except Exception as e:
            self.logger.error(f"PyMuPDFLoader Error: {type(e).__name__} - {str(e)}")
            return None, FileProcessingResponses.FILE_TEXT_EXTRACTION_FAILED.value
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        This function chunk documents and return chunks
        """
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = text_splitter.split_documents(documents=documents)
            return chunks, None
        except Exception as e:
            self.logger.error(f"Chunking Error: {type(e).__name__} - {str(e)}")
            return None, FileProcessingResponses.FILE_GENERIC_ERROR.value