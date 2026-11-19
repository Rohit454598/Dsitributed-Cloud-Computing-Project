import { useEffect, useState } from "react";
import {
  evaluateAnswer,
  listTextbooks,
  setTokenProvider,
  type EvaluateResult,
  type Textbook,
} from "./api/client";
import { useAuth } from "./auth/AuthContext";
import { AuthForm } from "./components/AuthForm";
import { EvaluateForm } from "./components/EvaluateForm";
import { EvaluationResult } from "./components/EvaluationResult";
import { HistoryPanel } from "./components/HistoryPanel";
import { TextbookUpload } from "./components/TextbookUpload";
import "./App.css";

function AuthenticatedApp() {
  const { user, profile, logout, getIdToken } = useAuth();
  const [textbooks, setTextbooks] = useState<Textbook[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [question, setQuestion] = useState("");
  const [studentAnswer, setStudentAnswer] = useState("");
  const [result, setResult] = useState<EvaluateResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [historyKey, setHistoryKey] = useState(0);

  useEffect(() => {
    setTokenProvider(getIdToken);
  }, [getIdToken]);

  useEffect(() => {
    if (!profile) return;
    listTextbooks()
      .then((books) => {
        setTextbooks(books);
        if (books[0]) setSelectedId(books[0].id);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Failed to load textbooks");
      });
  }, [profile]);

  async function handleEvaluate() {
    if (!selectedId || !question.trim() || !studentAnswer.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await evaluateAnswer({
        textbook_id: selectedId,
        question: question.trim(),
        student_answer: studentAnswer.trim(),
      });
      setResult(data);
      setHistoryKey((value) => value + 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Evaluation failed");
    } finally {
      setLoading(false);
    }
  }

  if (!profile) {
    return (
      <div className="page narrow">
        <div className="atmosphere" aria-hidden="true" />
        <header className="hero">
          <p className="brand">TextbookGrade</p>
          <h1>Finish setting up your profile</h1>
          <p className="lede">Signed in as {user?.email}. Choose a role to continue.</p>
        </header>
        <AuthForm mode="complete-profile" />
      </div>
    );
  }

  return (
    <div className="page">
      <div className="atmosphere" aria-hidden="true" />

      <header className="hero">
        <div className="hero-top">
          <p className="brand">TextbookGrade</p>
          <div className="user-chip">
            <span className="role-badge">{profile.role}</span>
            <span>{profile.display_name || profile.email}</span>
            <button type="button" className="ghost" onClick={() => void logout()}>
              Log out
            </button>
          </div>
        </div>
        <h1>Upload a textbook. Get graded against it.</h1>
        <p className="lede">
          Gemini retrieves the right passages, builds a model answer, then scores the student
          response with dynamic trait weights. History is saved to MongoDB for your account.
        </p>
      </header>

      <main className="layout">
        <div className="stack">
          <TextbookUpload
            textbooks={textbooks}
            selectedId={selectedId}
            onSelectedIdChange={setSelectedId}
            onTextbooksChange={setTextbooks}
          />
          <EvaluateForm
            question={question}
            studentAnswer={studentAnswer}
            disabled={!selectedId || !question.trim() || !studentAnswer.trim()}
            loading={loading}
            onQuestionChange={setQuestion}
            onStudentAnswerChange={setStudentAnswer}
            onSubmit={handleEvaluate}
          />
          {error && <p className="error banner">{error}</p>}
          <HistoryPanel key={historyKey} textbooks={textbooks} />
        </div>
        <EvaluationResult result={result} />
      </main>
    </div>
  );
}

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="page narrow">
        <div className="atmosphere" aria-hidden="true" />
        <p className="muted">Checking session…</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="page narrow">
        <div className="atmosphere" aria-hidden="true" />
        <header className="hero">
          <p className="brand">TextbookGrade</p>
          <h1>Sign in to grade against textbooks.</h1>
          <p className="lede">
            Teachers upload shared books. Students evaluate answers and keep history.
          </p>
        </header>
        <AuthForm />
      </div>
    );
  }

  return <AuthenticatedApp />;
}

export default App;
