from pathlib import Path

from pydantic import BaseModel, Field


class RawQuestionBlock(BaseModel):
    raw_prompts: list[str] = Field(default_factory=list)
    raw_answers: list[str] = Field(default_factory=list)
    source_line: int


class ParsedMarkdownFile(BaseModel):
    source_path: str
    unit_id: str
    part: str
    title: str | None = None
    items: list[RawQuestionBlock] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


def parse_markdown_file(path: Path) -> ParsedMarkdownFile:
    unit_id = path.parent.name
    part = path.stem
    lines = path.read_text(encoding="utf-8").splitlines()

    items: list[RawQuestionBlock] = []
    warnings: list[str] = []
    title: str | None = None
    current_prompts: list[str] = []
    current_answers: list[str] = []
    source_line = 1
    active_prompt_index: int | None = None

    def flush_block() -> None:
        nonlocal current_prompts, current_answers, source_line, active_prompt_index
        if not current_prompts and not current_answers:
            return
        if current_prompts and current_answers:
            items.append(
                RawQuestionBlock(
                    raw_prompts=current_prompts.copy(),
                    raw_answers=current_answers.copy(),
                    source_line=source_line,
                )
            )
        elif current_prompts:
            warnings.append(f"Line {source_line}: prompts without answer")
        else:
            warnings.append(f"Line {source_line}: answers without prompts")
        current_prompts = []
        current_answers = []
        active_prompt_index = None

    for index, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            flush_block()
            continue

        if line.startswith("#") and title is None:
            title = line.lstrip("#").strip()
            continue

        if line.startswith("*"):
            if not current_prompts and not current_answers:
                source_line = index
            elif current_answers:
                flush_block()
                source_line = index
            current_prompts.append(line.lstrip("*").strip())
            active_prompt_index = len(current_prompts) - 1
            continue

        if line.startswith("->"):
            if not current_prompts and not current_answers:
                source_line = index
            current_answers.append(line[2:].strip())
            active_prompt_index = None
            continue

        if active_prompt_index is not None and current_prompts:
            current_prompts[active_prompt_index] = f"{current_prompts[active_prompt_index]} {line}".strip()
        elif current_answers:
            current_answers[-1] = f"{current_answers[-1]} {line}".strip()
        else:
            warnings.append(f"Line {index}: ignored line '{line}'")

    flush_block()

    return ParsedMarkdownFile(
        source_path=str(path),
        unit_id=unit_id,
        part=part,
        title=title,
        items=items,
        warnings=warnings,
    )
