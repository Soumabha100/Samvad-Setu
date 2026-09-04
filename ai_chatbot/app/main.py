from fastapi import FastAPI
from .router import router as ai_router

app = FastAPI(title="Samvad-Setu AI Engine")
app.include_router(ai_router)

@app.get("/main")
def read_root():
    return {"status": "AI Engine is running"}
