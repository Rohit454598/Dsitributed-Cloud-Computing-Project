const API_BASE = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export type Textbook = {
  id: string;
  filename: string;
  chunk_count: number;
};

export type TraitWeights = {
  content_accuracy: number;
  coherence: number;
  vocabulary: number;
  grammar: number;
};

export type SourceChunk = {
  text: string;
  score: number | null;
};

export type EvaluateResult = {
  model_answer: string;
  sources: SourceChunk[];
  weights: TraitWeights;
  feedback: string;
  score: number | null;
};

async function parseError(response: Response): Promise<never> {
  let detail = `Request failed (${response.status})`;
  try {
    const data = await response.json();
    if (typeof data?.detail === "string") detail = data.detail;
    else if (Array.isArray(data?.detail)) {
      detail = data.detail.map((item: { msg?: string }) => item.msg ?? JSON.stringify(item)).join("; ");
    }
  } catch {
    /* ignore */
  }
  throw new Error(detail);
}

async function request(path: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(`${API_BASE}${path}`, init);
  } catch {
    throw new Error(
      `Cannot reach API at ${API_BASE}. Make sure the backend is running (uvicorn on port 8000).`,
    );
  }
}

export async function listTextbooks(): Promise<Textbook[]> {
  const response = await request("/api/textbooks");
  if (!response.ok) await parseError(response);
  return response.json();
}

export async function uploadTextbook(file: File): Promise<Textbook> {
  const form = new FormData();
  form.append("file", file);
  const response = await request("/api/textbooks", {
    method: "POST",
    body: form,
  });
  if (!response.ok) await parseError(response);
  return response.json();
}

export async function deleteTextbook(id: string): Promise<void> {
  const response = await request(`/api/textbooks/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) await parseError(response);
}

export async function evaluateAnswer(payload: {
  textbook_id: string;
  question: string;
  student_answer: string;
}): Promise<EvaluateResult> {
  const response = await request("/api/evaluate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) await parseError(response);
  return response.json();
}
