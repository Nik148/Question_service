from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from httpx import AsyncClient, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.schema import GenerateQuestionRequest, GenerateQuestionResponse
from app.database.model import Question
from app.database.core import get_session
from app.doc import generate_question_description


router = APIRouter(prefix="", tags=["Question"])

@router.post("/generate_question",
             response_model=List[GenerateQuestionResponse],
             description=generate_question_description)
async def generate_question(data: GenerateQuestionRequest, session: AsyncSession = Depends(get_session)):
    async with AsyncClient() as client:
        while True:
            response: Response = await client.get(
                f"https://jservice.io/api/random?count={data.questions_num}")
            models: List[Question] = [Question(id=item["id"],
                            answer=item["answer"],
                            question=item["question"],
                            created_at=datetime.strptime(item["created_at"], 
                                                         "%Y-%m-%dT%H:%M:%S.%fZ")
                            ) 
                    for item in response.json()]
            try:
                session.add_all(models)
                await session.commit()
            except:
                continue
            return models