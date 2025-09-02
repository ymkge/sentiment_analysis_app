from pydantic import BaseModel
from typing import List, Dict, Union

class SentimentDetail(BaseModel):
    label: str
    score: float

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    label: str
    score: float
    details: List[SentimentDetail]