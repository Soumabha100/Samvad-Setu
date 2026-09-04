from fastapi import APIRouter, HTTPException
from .schemes import (
    ChatRequest,
    ChatResponse,
    ClassificationRequest,
    ClassificationResponse,
    DuplicateCheckRequest,
    DuplicateCheckResponse
)
from .service import AIService
from .duplicate import check_duplicate

router = APIRouter(
    prefix="/api",
    tags=["AI"]
)

ai_service = AIService()


# chat responce from ai

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = ai_service.generate_response(request.message)
        return ChatResponse(status="success", response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")
 
#  classify 
@router.post("/classify", response_model=ClassificationResponse)
async def classify(request: ClassificationRequest):
    try:
        result = ai_service.classify_complaint(request.text)
        return ClassificationResponse(
            category=result.get("category", "other"),
            confidence=result.get("confidence", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")

# duplicate detection 

@router.post("/duplicate", response_model=DuplicateCheckResponse)
async def detect_duplicate(request: DuplicateCheckRequest):
    try:
        result = check_duplicate(request.text, threshold=request.threshold)
        return DuplicateCheckResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Duplicate detection error: {str(e)}")
