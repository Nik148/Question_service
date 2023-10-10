from pydantic import BaseModel, conint
from datetime import datetime


class GenerateQuestionRequest(BaseModel):
    questions_num: conint(ge=0)

class GenerateQuestionResponse(BaseModel):
    id: int
    answer: str
    question: str
    created_at: datetime

    class Config:
        from_attributes = True