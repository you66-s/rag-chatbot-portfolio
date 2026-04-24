from enum import Enum

class FileProcessingResponses(Enum):
    """
    This file contains messages responses related to file processing
    """
    FILE_GENERIC_ERROR = "An unexpected error occurred while processing your request. If the problem persists, please contact support."
    FILE_FORMAT_NOT_VALIDE = "File formate not supported, please provide a pdf file."
    FILE_SIZE_EXCEEDED = "You have exceeded the size limit, please a small file."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_STORAGE_FAIL = "Something went wrong. We couldn't save your file at this time."
    FILE_STORAGE_SUCCESS = "File stored successfully."
    FILE_SEARCH_BY_ID_NOT_FOUND = "File not found."
    FILE_TEXT_EXTRACTION_FAILED = "Could not extract content from the PDF file."