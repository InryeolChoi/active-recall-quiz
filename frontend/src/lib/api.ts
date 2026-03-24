import { ExamDetail, GradingResult, QuestionDetail, UnitSummary } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return (await response.json()) as T;
}

export function getUnits(): Promise<UnitSummary[]> {
  return request<UnitSummary[]>("/units");
}

export function getQuestions(): Promise<QuestionDetail[]> {
  return request<QuestionDetail[]>("/questions");
}

type CreateExamPayload = {
  unitIds?: string[];
  parts?: string[];
  questionCount?: number;
  mode?: "study" | "exam";
  shuffle?: boolean;
};

export function createExam(payload?: CreateExamPayload): Promise<ExamDetail> {
  return request<ExamDetail>("/exams", {
    method: "POST",
    body: JSON.stringify({
      unitIds: payload?.unitIds ?? [],
      parts: payload?.parts ?? [],
      questionCount: payload?.questionCount ?? 5,
      mode: payload?.mode ?? "exam",
      shuffle: payload?.shuffle ?? false
    })
  });
}

export function getExam(examId: string): Promise<ExamDetail> {
  return request<ExamDetail>(`/exams/${examId}`);
}

export function submitExam(examId: string, answers: { questionId: string; responseText: string }[]): Promise<GradingResult> {
  return request<GradingResult>(`/exams/${examId}/submit`, {
    method: "POST",
    body: JSON.stringify({ answers })
  });
}

export function getExamResult(examId: string): Promise<GradingResult> {
  return request<GradingResult>(`/exams/${examId}/result`);
}
