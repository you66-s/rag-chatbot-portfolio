from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from controllers.NLPController import NLPController
from controllers.FileController import FileController

nlp_route = APIRouter(prefix="/api/v1/nlp", tags=["NLP"])

# TODO: use dependancy injection instead of request

@nlp_route.post("/index/upload/{file_id}")
async def index_file(request: Request, file_id: str, collection_name: str, file_section: str, file_description: str):
    """
    File section is the resume section's informations holded by this file (skills, education.....)
    """
    nlp_controller = NLPController(vectord_db=request.app.state.vector_db, llm=request.app.state.llm)
    file_controller = FileController()
    # step 1: get file content
    documents, doc_msg = file_controller.file_content_loading(file_id=file_id)
    if documents is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=doc_msg
        )
    # step 2: chunk content and insert into vector db
    chunks, chunk_msg = file_controller.chunk_documents(documents=documents)
    if chunks is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=chunk_msg
        )
    for idx, chunk in enumerate(chunks):
        
        payload = {
            "text": chunk.page_content,
            "source": chunk.metadata["source"],
            "section": file_section,
            "description": file_description
        }
        is_inserted, message = nlp_controller.index_chunk(collection_name=collection_name, id=idx, chunk=chunk, payload=payload)
        if not is_inserted:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": message
        }
    )
@nlp_route.get("/search")
async def search_query(request: Request, query: str, collection_name: str):
    nlp_controller = NLPController(vectord_db=request.app.state.vector_db, llm=request.app.state.llm)
    search_result, search_msg = nlp_controller.retrieve_response(query=query, collection_name=collection_name)
    if search_result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=search_msg
        )
    return search_result