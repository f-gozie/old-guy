from typing import List

from pydantic import BaseModel


class Prediction(BaseModel):
    utterance: str
    time: int
    confidence: float
    model: str
