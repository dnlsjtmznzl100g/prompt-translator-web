// 반환 타입 정의
export interface TranslateResult {
  step1: string;
  step2: string;
  step3: string;
  step4: string;
}

// 환경변수로 API 기본 URL 관리
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * 번역 API 호출 함수
 * @param text - 번역할 텍스트
 * @param quality_mode - 번역 품질 옵션
 * @returns TranslateResult 타입의 4단계 번역 결과
 */
export async function translate(
  text: string,
  quality_mode: string
): Promise<TranslateResult> {
  try {
    const res = await fetch(`${API_BASE}/api/translate/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, quality_mode }),
    });

    if (!res.ok) {
      throw new Error(`Server Error: ${res.status} - ${res.statusText}`);
    }

    const data: TranslateResult = await res.json();
    return data;
  } catch (err) {
    console.error("Translate API Error:", err);
    throw err; // UI에서 처리 가능
  }
}

