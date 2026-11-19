# TextbookGrade

Upload a textbook, enter a question and student answer, and get graded feedback. The backend uses **Gemini + RAG** to auto-build the model answer from the uploaded book, then scores with dynamic trait weights.

**Auth:** Firebase Email/Password (teacher or student)  
**History / users / textbook metadata:** MongoDB

## Stack

- **Frontend:** React + Vite + TypeScript + Firebase Auth
- **Backend:** FastAPI + Firebase Admin
- **LLM / embeddings:** Google Gemini
- **Vector store:** local NumPy cosine store
- **Database:** MongoDB

## Setup

### 1. Gemini API key

```bash
cd backend
copy .env.example .env
```

Set `GEMINI_API_KEY` in `backend/.env`.

### 2. MongoDB

Use local MongoDB or [MongoDB Atlas](https://www.mongodb.com/atlas).

In `backend/.env`:

```
MONGODB_URI=mongodb://127.0.0.1:27017
MONGODB_DB=textbookgrade
```

For Atlas, paste your connection string into `MONGODB_URI`.

### 3. Firebase

1. Create a Firebase project and enable **Authentication → Email/Password**.
2. Create a Web app and copy the config into `frontend/.env`:

```bash
cd frontend
copy .env.example .env
```

```
VITE_API_URL=http://127.0.0.1:8000
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_AUTH_DOMAIN=...
VITE_FIREBASE_PROJECT_ID=...
VITE_FIREBASE_APP_ID=...
VITE_FIREBASE_STORAGE_BUCKET=...
VITE_FIREBASE_MESSAGING_SENDER_ID=...
```

3. Create a **service account** (Project settings → Service accounts → Generate new private key).
4. Save the JSON as `backend/firebase-service-account.json`  
   **or** paste the JSON into `FIREBASE_CREDENTIALS_JSON` in `backend/.env`.
5. Set `FIREBASE_PROJECT_ID` in `backend/.env`.

### 4. Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

### 5. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://127.0.0.1:5173

## Roles

- **Teacher:** upload up to 5 textbooks (shared with students); view evaluations on their books
- **Student:** see own + teacher-shared textbooks; evaluate answers; view personal history

## REST API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/health` | no | Health check |
| `POST` | `/api/auth/register-profile` | yes | Save role after Firebase signup |
| `GET` | `/api/auth/me` | yes | Current profile |
| `GET` | `/api/textbooks` | yes | List visible textbooks |
| `GET` | `/api/textbooks/quota` | yes | Used / max uploads |
| `POST` | `/api/textbooks` | yes | Upload PDF/TXT |
| `DELETE` | `/api/textbooks/{id}` | yes | Delete own textbook |
| `POST` | `/api/evaluate` | yes | RAG grade + save history |
| `GET` | `/api/evaluations/me` | yes | Own evaluation history |
| `GET` | `/api/evaluations/textbook/{id}` | teacher | Evaluations for owned textbook |

Send `Authorization: Bearer <Firebase ID token>` on protected routes.

## Flow

1. Sign up / sign in with Firebase (choose teacher or student)
2. Upload textbook → chunk → Gemini embeddings → local vectors + Mongo metadata
3. Evaluate → retrieve chunks → model answer → weighted feedback → save evaluation in MongoDB

## Notes

- Max **5 textbooks per user**
- Supported uploads: `.pdf`, `.txt`
- Never commit `.env`, `firebase-service-account.json`, or API keys
