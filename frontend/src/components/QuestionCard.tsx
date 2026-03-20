type Props = {
  index?: number;
  prompts: string[];
  meta?: string;
  children?: React.ReactNode;
};

export function QuestionCard({ index, prompts, meta, children }: Props) {
  return (
    <section className="question-card stack">
      {typeof index === "number" ? <div className="badge">문제 {index + 1}</div> : null}
      {meta ? <p className="muted">{meta}</p> : null}
      <div className="stack">
        {prompts.map((prompt, promptIndex) => (
          <p key={`${promptIndex}-${prompt}`}>{prompt}</p>
        ))}
      </div>
      {children}
    </section>
  );
}
