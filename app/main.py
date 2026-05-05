from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.file import file_route
from routes.nlp import nlp_route
from store.llm.GeminiProvider import GeminiProvider
from store.vectordb.QdrantProvider import QdrantProvider
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # RAG COMPONENTS
    app.state.llm = GeminiProvider()
    app.state.vector_db = QdrantProvider()
    logger.info("RAG components started...")
    yield
    logger.info("RAG components stopped.")


app = FastAPI(title="Chatbot As Portfolio", lifespan=lifespan)
app.include_router(file_route)
app.include_router(nlp_route)