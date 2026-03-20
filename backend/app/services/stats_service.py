from app.schemas.grading import WeaknessPoint, WeaknessStats
from app.services.exam_service import _result_store


class StatsService:
    def get_weakness_stats(self) -> WeaknessStats:
        unit_wrong_counts: dict[str, int] = {}
        question_wrong_counts: dict[str, int] = {}
        keyword_wrong_counts: dict[str, int] = {}

        for result in _result_store.values():
            for question in result.results:
                if question.isCorrect:
                    continue
                question_wrong_counts[question.questionId] = question_wrong_counts.get(question.questionId, 0) + 1
                unit_id = question.questionId.split(":")[0]
                unit_wrong_counts[unit_id] = unit_wrong_counts.get(unit_id, 0) + 1
                for keyword in question.missingKeywords:
                    keyword_wrong_counts[keyword] = keyword_wrong_counts.get(keyword, 0) + 1

        return WeaknessStats(
            weakUnits=[
                WeaknessPoint(name=unit_id, value=count)
                for unit_id, count in sorted(unit_wrong_counts.items(), key=lambda item: item[1], reverse=True)
            ],
            weakQuestions=[
                WeaknessPoint(name=question_id, value=count)
                for question_id, count in sorted(question_wrong_counts.items(), key=lambda item: item[1], reverse=True)
            ],
            weakKeywords=[
                WeaknessPoint(name=keyword, value=count)
                for keyword, count in sorted(keyword_wrong_counts.items(), key=lambda item: item[1], reverse=True)
            ],
        )
