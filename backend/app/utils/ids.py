def build_question_id(unit_id: str, part: str, offset: int) -> str:
    return f"{unit_id}:{part}:{offset}"
