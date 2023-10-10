from httpx import AsyncClient
from sqlalchemy import select
import pytest
from typing import List
from .conftest import async_session_maker
from app.database.model import Question


@pytest.mark.asyncio
async def test_generate_question(ac: AsyncClient):
    response = await ac.post("/generate_question", json={
        "questions_num": 0
    })
    
    assert response.status_code == 200
    assert len(response.json()) == 0
    # async with async_session_maker() as session:
    #     user = await session.execute(select(User).where(User.login == "lake"))
    #     user: User = user.scalar()
    #     assert user
    response = await ac.post("/generate_question", json={
        "questions_num": -2
    })
    
    assert response.status_code == 422

    response = await ac.post("/generate_question", json={
        "questions_num": 3
    })
    
    assert response.status_code == 200
    assert len(response.json()) == 3

    async with async_session_maker() as session:
        questions = await session.execute(select(Question))
        questions: List[Question] = questions.scalars().all()
        assert len(questions) == 3

    