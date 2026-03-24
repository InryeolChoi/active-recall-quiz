import { GradingResult, WrongNoteEntry } from "@/lib/types";

export const WRONG_NOTE_STORAGE_KEY = "active-recall-quiz/wrong-notes";

function canUseStorage(): boolean {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

export function readWrongNotes(): WrongNoteEntry[] {
  if (!canUseStorage()) {
    return [];
  }

  const rawValue = window.localStorage.getItem(WRONG_NOTE_STORAGE_KEY);
  if (!rawValue) {
    return [];
  }

  try {
    const parsed = JSON.parse(rawValue) as WrongNoteEntry[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function writeWrongNotes(entries: WrongNoteEntry[]): void {
  if (!canUseStorage()) {
    return;
  }

  window.localStorage.setItem(WRONG_NOTE_STORAGE_KEY, JSON.stringify(entries));
}

export function appendWrongNotesFromResult(result: GradingResult): number {
  const wrongEntries = result.results
    .filter((item) => !item.isCorrect)
    .map<WrongNoteEntry>((item) => ({
      id: `${result.examId}:${item.questionId}`,
      savedAt: result.submittedAt,
      examId: result.examId,
      questionId: item.questionId,
      type: item.type,
      userAnswer: item.userAnswer,
      expectedAnswers: item.expectedAnswers,
      feedback: item.feedback,
      missingKeywords: item.missingKeywords
    }));

  if (wrongEntries.length === 0) {
    return 0;
  }

  const existingEntries = readWrongNotes();
  const entryMap = new Map(existingEntries.map((entry) => [entry.id, entry]));
  wrongEntries.forEach((entry) => entryMap.set(entry.id, entry));
  writeWrongNotes(Array.from(entryMap.values()).sort((left, right) => right.savedAt.localeCompare(left.savedAt)));
  return wrongEntries.length;
}
