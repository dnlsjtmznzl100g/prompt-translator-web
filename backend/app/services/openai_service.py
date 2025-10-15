import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def translate_text(text: str, quality_mode: str):
    # 단순 예제, 4단계 번역 구조
    steps = ["Step 1", "Step 2", "Step 3", "Step 4"]
    result = {}
    for i, step in enumerate(steps, start=1):
        # 실제 GPT 호출은 필요시 수정
        result[f"step{i}"] = f"{step}: {text} (translated, mode={quality_mode})"
    return result




