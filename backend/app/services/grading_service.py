from app.schemas.exam import ExamQuestion
from app.schemas.grading import QuestionGradingResult
from app.utils.text_norm import normalize_text


class GradingService:
    def grade_question(self, question: ExamQuestion, response_text: str) -> QuestionGradingResult:
        if question.type == "list_answer":
            return self._grade_list_answer(question, response_text)
        return self._grade_short_answer(question, response_text)

    def _grade_short_answer(self, question: ExamQuestion, response_text: str) -> QuestionGradingResult:
        normalized_response = normalize_text(response_text)
        normalized_answers = [normalize_text(answer) for answer in question.answersSnapshot]
        normalized_aliases = [normalize_text(alias) for alias in question.aliasesSnapshot]
        is_correct = normalized_response in normalized_answers or normalized_response in normalized_aliases
        earned_score = question.maxScore if is_correct else 0
        return QuestionGradingResult(
            questionId=question.questionId,
            type=question.type,
            isCorrect=is_correct,
            earnedScore=earned_score,
            maxScore=question.maxScore,
            userAnswer=response_text,
            expectedAnswers=question.answersSnapshot,
            matchedKeywords=[],
            missingKeywords=[] if is_correct else question.keywordsSnapshot,
            feedback="정답입니다." if is_correct else "정답과 일치하지 않습니다.",
        )

    def _grade_list_answer(self, question: ExamQuestion, response_text: str) -> QuestionGradingResult:
        normalized_response = normalize_text(response_text)
        matched = [
            keyword
            for keyword in question.keywordsSnapshot
            if keyword and normalize_text(keyword) in normalized_response
        ]
        unique_matched = list(dict.fromkeys(matched))
        total_keywords = max(len(question.keywordsSnapshot), 1)
        ratio = len(unique_matched) / total_keywords
        earned_score = round(question.maxScore * ratio)
        is_correct = len(unique_matched) == total_keywords
        missing = [keyword for keyword in question.keywordsSnapshot if keyword not in unique_matched]
        feedback = "모든 핵심 항목을 포함했습니다." if is_correct else "일부 핵심 항목이 누락되었습니다."
        return QuestionGradingResult(
            questionId=question.questionId,
            type=question.type,
            isCorrect=is_correct,
            earnedScore=earned_score,
            maxScore=question.maxScore,
            userAnswer=response_text,
            expectedAnswers=question.answersSnapshot,
            matchedKeywords=unique_matched,
            missingKeywords=missing,
            feedback=feedback,
        )
