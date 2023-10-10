from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .core import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    answer = Column(String)
    question = Column(String)
    created_at = Column(DateTime)

    def __init__(self, id: int, answer: str, question: str, created_at: datetime):
        self.id = id
        self.answer = answer
        self.question = question
        self.created_at = created_at