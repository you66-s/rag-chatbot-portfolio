from fastapi import FastAPI
from routes.file import file_route


app = FastAPI(title="Chatbot As Portfolio")
app.include_router(file_route)