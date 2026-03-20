import re

from app.parsers.markdown_parser import ParsedMarkdownFile
from app.schemas.question import QuestionDetail
from app.utils.ids import build_question_id

LIST_SPLIT_PATTERN = re.compile(r"\s*,\s*")
NUMBERED_PREFIX_PATTERN = re.compile(r"^\d+\.\s*")
PAREN_ALIAS_PATTERN = re.compile(r"^(?P<main>.+?)\((?P<alias>.+?)\)$")


def normalize_parsed_file(parsed: ParsedMarkdownFile) -> list[QuestionDetail]:
    questions: list[QuestionDetail] = []
    for offset, item in enumerate(parsed.items, start=1):
        answers = [_clean_answer(answer) for answer in item.raw_answers if answer.strip()]
        aliases = _extract_aliases(answers)
        keywords = _extract_keywords(answers)
        question_type = "list_answer" if len(answers) > 1 else "short_answer"
        questions.append(
            QuestionDetail(
                questionId=build_question_id(parsed.unit_id, parsed.part, offset),
                unitId=parsed.unit_id,
                part=parsed.part,
                title=parsed.title,
                type=question_type,
                prompts=[prompt.strip() for prompt in item.raw_prompts if prompt.strip()],
                answers=answers,
                aliases=aliases,
                keywords=keywords,
                warnings=parsed.warnings,
                sourcePath=parsed.source_path,
                sourceLine=item.source_line,
            )
        )
    return questions


def _clean_answer(answer: str) -> str:
    answer = NUMBERED_PREFIX_PATTERN.sub("", answer.strip())
    return re.sub(r"\s+", " ", answer)


def _extract_aliases(answers: list[str]) -> list[str]:
    aliases: list[str] = []
    for answer in answers:
        match = PAREN_ALIAS_PATTERN.match(answer)
        if match:
            aliases.append(match.group("alias").strip())
    return aliases


def _extract_keywords(answers: list[str]) -> list[str]:
    keywords: list[str] = []
    for answer in answers:
        pieces = LIST_SPLIT_PATTERN.split(answer)
        if len(pieces) > 1:
            keywords.extend(piece for piece in pieces if piece)
        else:
            keywords.append(answer)
    return keywords
