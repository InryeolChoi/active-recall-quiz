"use client";

type Props = {
  value: string;
  onChange: (nextValue: string) => void;
};

export function AnswerInput({ value, onChange }: Props) {
  return (
    <textarea
      placeholder="여기에 직접 서술형 답안을 적어보세요."
      value={value}
      onChange={(event) => onChange(event.target.value)}
    />
  );
}
