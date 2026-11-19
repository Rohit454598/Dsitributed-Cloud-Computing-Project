import { useEffect, useState } from "react";
import {
  evaluateAnswer,
  listTextbooks,
  type EvaluateResult,
  type Textbook,
} from "./api/client";
import { EvaluateForm } from "./components/EvaluateForm";
import { EvaluationResult } from "./components/EvaluationResult";
import { TextbookUpload } from "./components/TextbookUpload";
import "./App.css";

function App() {
  const [textbooks, setTextbooks] = useState<Textbook[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [question, setQuestion] = useState("");
  const [studentAnswer, setStudentAnswer] = useState("");
  const [result, setResult] = useState<EvaluateResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listTextbooks()
      .then((books) => {
        setTextbooks(books);
        if (books[0]) setSelectedId(books[0].id);
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Failed to load textbooks");
      });
  }, []);

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
    } catch (err) {
      setError(err instanceof Error ? err.message : "Evaluation failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="atmosphere" aria-hidden="true" />

      <header className="hero">
        <p className="brand">TextbookGrade</p>
        <h1>Upload a textbook. Get graded against it.</h1>
        <p className="lede">
          Gemini retrieves the right passages, builds a model answer, then scores the student
          response with dynamic trait weights.
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
        </div>
        <EvaluationResult result={result} />
      </main>
    </div>
  );
}

export default App;
