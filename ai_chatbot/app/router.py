from fastapi import APIRouter, HTTPException
from .schemes import ChatRequest, ChatResponse, ClassificationRequest, ClassificationResponse
from .service import AIService

router = APIRouter(
    prefix="/api",
    tags=["AI"]
)

ai_service = AIService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer = ai_service.generate_response(request.message)
        return ChatResponse(status="success", response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

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
