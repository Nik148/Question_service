from fastapi import FastAPI
from app.routers import router


tags_metadata = [
    {
        "name": "Question",
        "description": "Операции связанные с 'Question'",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(router)