import { useEffect, useRef, useState } from "react";
import type { Textbook } from "../api/client";
import { deleteTextbook, getTextbookQuota, uploadTextbook } from "../api/client";

type Props = {
  textbooks: Textbook[];
  selectedId: string;
  onSelectedIdChange: (id: string) => void;
  onTextbooksChange: (books: Textbook[]) => void;
};

export function TextbookUpload({
  textbooks,
  selectedId,
  onSelectedIdChange,
  onTextbooksChange,
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [quota, setQuota] = useState<{ used: number; max: number; remaining: number } | null>(
    null,
  );

  async function refreshQuota() {
    try {
      setQuota(await getTextbookQuota());
    } catch {
      setQuota(null);
    }
  }

  useEffect(() => {
    void refreshQuota();
  }, [textbooks]);

  async function handleUpload(file: File | undefined) {
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      const book = await uploadTextbook(file);
      onTextbooksChange([book, ...textbooks.filter((b) => b.id !== book.id)]);
      onSelectedIdChange(book.id);
      await refreshQuota();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  async function handleDelete(id: string) {
    setError(null);
    try {
      await deleteTextbook(id);
      const next = textbooks.filter((book) => book.id !== id);
      onTextbooksChange(next);
      if (selectedId === id) onSelectedIdChange(next[0]?.id ?? "");
      await refreshQuota();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  return (
    <section className="panel">
      <div className="panel-head">
        <h2>Textbook</h2>
        <p>
          Upload a PDF or TXT. Teachers share books with students. Limit:{" "}
          {quota ? `${quota.used}/${quota.max}` : "5"} per user.
        </p>
      </div>

      <div className="upload-row">
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt,application/pdf,text/plain"
          disabled={uploading || (quota != null && quota.remaining <= 0)}
          onChange={(event) => handleUpload(event.target.files?.[0])}
        />
        {uploading && <span className="muted">Indexing with Gemini…</span>}
      </div>

      {error && <p className="error">{error}</p>}

      {textbooks.length > 0 ? (
        <ul className="book-list">
          {textbooks.map((book) => (
            <li key={book.id} className={book.id === selectedId ? "active" : ""}>
              <button
                type="button"
                className="book-select"
                onClick={() => onSelectedIdChange(book.id)}
              >
                <strong>{book.filename}</strong>
                <span>
                  {book.chunk_count} chunks
                  {book.owned_by_me
                    ? " · yours"
                    : book.owner_role === "teacher"
                      ? " · teacher shared"
                      : ""}
                </span>
              </button>
              {book.owned_by_me && (
                <button
                  type="button"
                  className="ghost danger"
                  onClick={() => handleDelete(book.id)}
                >
                  Remove
                </button>
              )}
            </li>
          ))}
        </ul>
      ) : (
        <p className="muted">No textbooks available yet.</p>
      )}
    </section>
  );
}
