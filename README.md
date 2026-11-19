# TextbookGrade

Upload a textbook, enter a question and student answer, and get graded feedback. The backend uses **Gemini + RAG** to automatically build a model answer from the uploaded textbook, then evaluates the student's response using dynamic trait weights.

## Tech Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI
- **LLM:** Google Gemini
- **Embeddings:** Gemini embeddings
- **Vector Store:** Local NumPy cosine similarity store (no C++ build tools required)

## Features

- Upload textbooks in PDF or TXT format
- Automatically chunk and index textbook content
- Retrieve relevant textbook passages using semantic similarity
- Generate textbook-grounded model answers
- Evaluate student answers using dynamic trait weights
- Provide explainable feedback and scores out of 10

## Setup

### 1. Configure Gemini API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

Navigate to the backend folder:

```bash
cd backend
copy .env.example .env
```

Edit `backend/.env` and add your API key:

```env
GEMINI_API_KEY=your_key_here
```

### 2. Start the Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

### 3. Start the Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Application:

http://127.0.0.1:5173

## REST API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/textbooks` | List indexed textbooks |
| POST | `/api/textbooks` | Upload PDF/TXT textbook |
| DELETE | `/api/textbooks/{id}` | Remove textbook and vectors |
| POST | `/api/evaluate` | Generate model answer and evaluate student answer |

### Evaluation Request

`POST /api/evaluate`

```json
{
  "textbook_id": "uuid",
  "question": "Explain how neural networks work.",
  "student_answer": "Your answer here"
}
```

### Evaluation Response

- **model_answer** — Model answer generated from retrieved textbook content
- **sources** — Retrieved textbook passages
- **weights** — Dynamically assigned evaluation trait weights
- **feedback** — Explainable feedback on the student's answer
- **score** — Overall score out of 10

## System Workflow

1. Upload textbook (PDF/TXT).
2. Extract text and split it into chunks.
3. Generate embeddings and store them in the local vector store.
4. Retrieve the most relevant textbook chunks for a question.
5. Gemini generates a model answer grounded in the retrieved passages.
6. Gemini evaluates the student's answer using dynamic trait weights.
7. Return the score, feedback, model answer, and relevant sources.

## Notes

- Supported file formats: `.pdf` and `.txt`
- Keep your `GEMINI_API_KEY` in the `.env` file.
- Never commit API keys or secrets to GitHub.
- If a previously exposed Mistral API key is still active, revoke it.

---

**Distributed Cloud Computing Project**
