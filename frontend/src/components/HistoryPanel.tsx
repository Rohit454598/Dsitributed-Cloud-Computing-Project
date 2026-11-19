import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import {
  listMyEvaluations,
  listTextbookEvaluations,
  type EvaluationRecord,
  type Textbook,
} from "../api/client";

type Props = {
  textbooks: Textbook[];
};

export function HistoryPanel({ textbooks }: Props) {
  const { profile } = useAuth();
  const [items, setItems] = useState<EvaluationRecord[]>([]);
  const [selectedTextbookId, setSelectedTextbookId] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const ownedBooks = textbooks.filter((book) => book.owned_by_me);

  useEffect(() => {
    if (profile?.role === "teacher" && ownedBooks[0] && !selectedTextbookId) {
      setSelectedTextbookId(ownedBooks[0].id);
    }
  }, [profile?.role, ownedBooks, selectedTextbookId]);

  useEffect(() => {
    async function load() {
      if (!profile) return;
      setLoading(true);
      setError(null);
      try {
        if (profile.role === "teacher") {
          if (!selectedTextbookId) {
            setItems([]);
            return;
          }
          setItems(await listTextbookEvaluations(selectedTextbookId));
        } else {
          setItems(await listMyEvaluations());
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load history");
      } finally {
        setLoading(false);
      }
    }
    void load();
  }, [profile, selectedTextbookId]);

  return (
    <section className="panel">
      <div className="panel-head">
        <h2>History</h2>
        <p>
          {profile?.role === "teacher"
            ? "Evaluations submitted against your textbooks."
            : "Your past questions, answers, and feedback."}
        </p>
      </div>

      {profile?.role === "teacher" && (
        <label className="field">
          <span>Textbook</span>
          <select
            value={selectedTextbookId}
            onChange={(e) => setSelectedTextbookId(e.target.value)}
          >
            {ownedBooks.length === 0 && <option value="">No textbooks yet</option>}
            {ownedBooks.map((book) => (
              <option key={book.id} value={book.id}>
                {book.filename}
              </option>
            ))}
          </select>
        </label>
      )}

      {loading && <p className="muted">Loading history…</p>}
      {error && <p className="error">{error}</p>}

      {!loading && items.length === 0 && (
        <p className="muted">No evaluations saved yet.</p>
      )}

      <ul className="history-list">
        {items.map((item) => (
          <li key={item.id}>
            <div className="history-top">
              <strong>{item.textbook_filename || item.textbook_id}</strong>
              <span>{item.score != null ? `${item.score}/10` : "—"}</span>
            </div>
            <p className="history-q">{item.question}</p>
            <details>
              <summary>View details</summary>
              <p>
                <strong>Student answer</strong>
              </p>
              <pre className="feedback compact">{item.student_answer}</pre>
              <p>
                <strong>Feedback</strong>
              </p>
              <pre className="feedback compact">{item.feedback}</pre>
            </details>
          </li>
        ))}
      </ul>
    </section>
  );
}
