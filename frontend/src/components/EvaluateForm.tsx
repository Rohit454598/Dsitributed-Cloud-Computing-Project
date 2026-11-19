type Props = {
  question: string;
  studentAnswer: string;
  disabled: boolean;
  loading: boolean;
  onQuestionChange: (value: string) => void;
  onStudentAnswerChange: (value: string) => void;
  onSubmit: () => void;
};

export function EvaluateForm({
  question,
  studentAnswer,
  disabled,
  loading,
  onQuestionChange,
  onStudentAnswerChange,
  onSubmit,
}: Props) {
  return (
    <section className="panel">
      <div className="panel-head">
        <h2>Evaluate</h2>
        <p>Enter the question and the student answer. The model answer is built from the textbook.</p>
      </div>

      <label className="field">
        <span>Question</span>
        <textarea
          rows={3}
          value={question}
          onChange={(event) => onQuestionChange(event.target.value)}
          placeholder="Explain the key features of the Indus Valley Civilization."
        />
      </label>

      <label className="field">
        <span>Student answer</span>
        <textarea
          rows={8}
          value={studentAnswer}
          onChange={(event) => onStudentAnswerChange(event.target.value)}
          placeholder="Paste the student's response here…"
        />
      </label>

      <button
        type="button"
        className="primary"
        disabled={disabled || loading}
        onClick={onSubmit}
      >
        {loading ? "Building model answer & grading…" : "Evaluate answer"}
      </button>
    </section>
  );
}
