from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    status: str
    response: str

class ClassificationRequest(BaseModel):
    text: str

class ClassificationResponse(BaseModel):
    category: str
    confidence: float

class DuplicateCheckRequest(BaseModel):
    text: str
    threshold: Optional[float] = 0.85

class DuplicateCheckResponse(BaseModel):
    isDuplicate: bool
    similarity: float
    matchedComplaintId: Optional[str] = None
    matchedComplaintText: Optional[str] = None

