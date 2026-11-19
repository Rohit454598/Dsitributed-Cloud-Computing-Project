import type { EvaluateResult } from "../api/client";

type Props = {
  result: EvaluateResult | null;
};

export function EvaluationResult({ result }: Props) {
  if (!result) {
    return (
      <section className="panel result-empty">
        <div className="panel-head">
          <h2>Result</h2>
          <p>Run an evaluation to see the RAG model answer, sources, weights, and feedback.</p>
        </div>
      </section>
    );
  }

  const { weights } = result;

  return (
    <section className="panel result">
      <div className="panel-head score-row">
        <div>
          <h2>Result</h2>
          <p>Model answer was retrieved and generated from the uploaded textbook.</p>
        </div>
        <div className="score-badge">
          <span>Score</span>
          <strong>{result.score != null ? `${result.score}/10` : "—"}</strong>
        </div>
      </div>

      <div className="weights">
        <div>
          <span>Content</span>
          <strong>{weights.content_accuracy}%</strong>
        </div>
        <div>
          <span>Coherence</span>
          <strong>{weights.coherence}%</strong>
        </div>
        <div>
          <span>Vocabulary</span>
          <strong>{weights.vocabulary}%</strong>
        </div>
        <div>
          <span>Grammar</span>
          <strong>{weights.grammar}%</strong>
        </div>
      </div>

      <article>
        <h3>Model answer</h3>
        <p className="body-text">{result.model_answer}</p>
      </article>

      <article>
        <h3>Improvement feedback</h3>
        <p className="muted">Mistakes and trait-based tips only — what to fix next.</p>
        <pre className="feedback">{result.feedback}</pre>
      </article>

      <article>
        <h3>Sources used</h3>
        <ol className="sources">
          {result.sources.map((source, index) => (
            <li key={`${index}-${source.score ?? 0}`}>
              {source.score != null && (
                <span className="muted">similarity {source.score}</span>
              )}
              <p>{source.text}</p>
            </li>
          ))}
        </ol>
      </article>
    </section>
  );
}
