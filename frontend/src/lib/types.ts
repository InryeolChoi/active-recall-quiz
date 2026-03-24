export type QuestionType = "short_answer" | "list_answer";

export type UnitSummary = {
  unitId: string;
  title: string;
  parts: string[];
  questionCount: number;
};

export type QuestionDetail = {
  questionId: string;
  unitId: string;
  part: string;
  title?: string | null;
  type: QuestionType;
  prompts: string[];
  answers: string[];
  aliases: string[];
  keywords: string[];
  warnings: string[];
  sourcePath: string;
  sourceLine: number;
};

export type ExamQuestion = {
  questionId: string;
  unitId: string;
  part: string;
  type: QuestionType;
  prompts: string[];
  answersSnapshot: string[];
  aliasesSnapshot: string[];
  keywordsSnapshot: string[];
  maxScore: number;
};

export type ExamDetail = {
  examId: string;
  mode: "study" | "exam";
  createdAt: string;
  unitIds: string[];
  parts: string[];
  questionCount: number;
  questions: ExamQuestion[];
};

export type QuestionGradingResult = {
  questionId: string;
  type: QuestionType;
  isCorrect: boolean;
  earnedScore: number;
  maxScore: number;
  userAnswer: string;
  expectedAnswers: string[];
  matchedKeywords: string[];
  missingKeywords: string[];
  feedback: string;
};

export type GradingResult = {
  examId: string;
  score: number;
  total: number;
  submittedAt: string;
  results: QuestionGradingResult[];
};

export type WrongNoteEntry = {
  id: string;
  savedAt: string;
  examId: string;
  questionId: string;
  type: QuestionType;
  userAnswer: string;
  expectedAnswers: string[];
  feedback: string;
  missingKeywords: string[];
};
