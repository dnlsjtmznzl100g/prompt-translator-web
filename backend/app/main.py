from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import translate

app = FastAPI(title="Prompt Translator Web API")

# CORS 설정 (React dev 서버 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(translate.router, prefix="/api/translate")

@app.get("/")
async def root():
    return {"message": "Prompt Translator Web API is running."}
