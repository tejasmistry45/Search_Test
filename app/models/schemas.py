from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class AnswerResponse(BaseModel):
    answer: str
    citations: List[str]
