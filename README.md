# TextbookGrade

Upload a textbook, enter a question and student answer, and get graded feedback. The backend uses **Gemini + RAG** (ChromaDB) to auto-build the model answer from the uploaded book, then scores with dynamic trait weights.

## Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI
- **LLM / embeddings:** Google Gemini
- **Vector store:** local NumPy cosine store (no C++ build tools required)

## Setup

### 1. Gemini API key

1. Get a key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Copy the backend env file and add your key:

```bash
cd backend
copy .env.example .env
```

Edit `backend/.env`:

```
GEMINI_API_KEY=your_key_here
```

### 2. Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

API docs: http://127.0.0.1:8000/docs

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://127.0.0.1:5173

## REST API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/textbooks` | List indexed textbooks |
| `POST` | `/api/textbooks` | Upload PDF/TXT (multipart `file`) |
| `DELETE` | `/api/textbooks/{id}` | Remove textbook + vectors |
| `POST` | `/api/evaluate` | RAG model answer + evaluation |

### Evaluate body

```json
{
  "textbook_id": "uuid",
  "question": "Explain how neural networks work.",
  "student_answer": "..."
}
```

### Evaluate response

- `model_answer` — generated from retrieved textbook chunks
- `sources` — retrieved passages
- `weights` — dynamic trait weights
- `feedback` — explainable grading text
- `score` — overall score out of 10 (parsed when present)

## Flow

1. Upload textbook → chunk → Gemini embeddings → local vector store
2. On evaluate → retrieve top-k chunks for the question
3. Gemini writes a model answer grounded in those chunks
4. Gemini assigns trait weights and grades the student answer

## Notes

- Supported uploads: `.pdf`, `.txt`
- Keep `GEMINI_API_KEY` in `.env` only — never hardcode keys
- If you previously shared a Mistral key in a notebook, revoke it
