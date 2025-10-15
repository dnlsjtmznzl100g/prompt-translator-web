import os
import openai
import asyncio
from dotenv import load_dotenv
from typing import Dict, Literal

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

QualityMode = Literal["neutral", "high", "fast"]

# temperature 맵핑
QUALITY_TEMPERATURE = {
    "neutral": 0.6,
    "high": 0.8,
    "fast": 0.4,
}


def preprocess_text(text: str) -> str:
    """
    체크포인트 자동 보완:
    - 문장이 너무 짧거나 모호하면 보완
    - 맥락/대상/말투 등 누락 시 안내
    """
    text = text.strip()
    if len(text) < 5:
        text += " Please provide more details."
    if "?" in text and not text.endswith("?"):
        text += "?"
    return text


async def _call_gpt_with_retry(messages, model: str, temperature: float, retries: int = 3, delay: float = 1.0):
    """
    GPT 호출 재시도 로직
    """
    for attempt in range(1, retries + 1):
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError as e:
            if attempt == retries:
                raise
            await asyncio.sleep(delay * attempt)  # 지수 백오프
        except openai.error.APIError as e:
            if attempt == retries:
                raise
            await asyncio.sleep(delay)
        except openai.error.APIConnectionError as e:
            if attempt == retries:
                raise
            await asyncio.sleep(delay)
        except openai.error.Timeout as e:
            if attempt == retries:
                raise
            await asyncio.sleep(delay)
    return "[Error]: GPT call failed after retries."


async def translate_text(text: str, quality_mode: QualityMode = "neutral") -> Dict[str, str]:
    """
    단일 GPT 호출로 4단계 번역 수행 + 체크포인트 자동 보완 + quality_mode 기반 temperature 적용
    """
    text = preprocess_text(text)
    temperature = QUALITY_TEMPERATURE.get(quality_mode, 0.6)

    # 4단계 번역 요청을 한 번의 GPT 호출로 처리
    system_prompt = f"""
    You are an expert English translator.
    Translate the following Korean text to English in 4 steps.
    Quality mode: {quality_mode}
    
    Step 1: Straightforward translation
    Step 2: Slightly rephrase with different word choice
    Step 3: Add extra conditions or clarifications if needed
    Step 4: Restructure sentence for natural flow

    Respond in the following JSON format exactly:
    {{
        "step1": "...",
        "step2": "...",
        "step3": "...",
        "step4": "..."
    }}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    try:
        response_text = await _call_gpt_with_retry(
            messages=messages,
            model="gpt-4o-mini",
            temperature=temperature
        )
        # GPT 응답을 dict로 변환
        import json
        steps = json.loads(response_text) 
    except Exception as e:
        steps = {
            "step1": f"[Error]: {str(e)}",
            "step2": f"[Error]: {str(e)}",
            "step3": f"[Error]: {str(e)}",
            "step4": f"[Error]: {str(e)}"
        }

    return steps
