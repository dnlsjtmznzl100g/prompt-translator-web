# backend/app/routes/translate.py

from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.openai_service import translate_text

router = APIRouter()

class QualityMode(str, Enum):
    """번역 품질 모드 제한"""
    normal = "normal"
    high = "high"
    custom = "custom"

class TranslateRequest(BaseModel):
    """클라이언트에서 받는 번역 요청 모델"""
    text: str
    quality_mode: QualityMode = QualityMode.normal

class TranslateResponse(BaseModel):
    """4단계 번역 결과 모델"""
    step1: str
    step2: str
    step3: str
    step4: str

@router.post("/", response_model=TranslateResponse)
async def translate(req: TranslateRequest):
    """
    번역 API 엔드포인트
    - text: 번역할 문장
    - quality_mode: 번역 품질 선택
    - 반환: step1~step4 영어 번역 결과
    """
    try:
        translations = await translate_text(req.text, req.quality_mode)
        return translations
    except Exception as e:
        # OpenAI 호출 실패나 네트워크 오류 처리
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

