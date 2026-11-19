const API_BASE = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

let tokenProvider: (() => Promise<string | null>) | null = null;

export function setTokenProvider(provider: () => Promise<string | null>) {
  tokenProvider = provider;
}

export type Textbook = {
  id: string;
  filename: string;
  chunk_count: number;
  user_id?: string | null;
  owner_role?: string | null;
  shared?: boolean;
  owned_by_me?: boolean;
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
  id?: string | null;
  model_answer: string;
  sources: SourceChunk[];
  weights: TraitWeights;
  feedback: string;
  score: number | null;
};

export type UserProfile = {
  uid: string;
  email: string;
  role: "teacher" | "student" | string;
  display_name: string;
};

export type EvaluationRecord = {
  id: string;
  user_id: string;
  textbook_id: string;
  textbook_owner_id: string;
  textbook_filename?: string | null;
  question: string;
  student_answer: string;
  model_answer: string;
  sources: SourceChunk[];
  weights: TraitWeights;
  feedback: string;
  score: number | null;
  created_at?: string | null;
};

async function parseError(response: Response): Promise<never> {
  let detail = `Request failed (${response.status})`;
  try {
    const data = await response.json();
    if (typeof data?.detail === "string") detail = data.detail;
    else if (Array.isArray(data?.detail)) {
      detail = data.detail
        .map((item: { msg?: string }) => item.msg ?? JSON.stringify(item))
        .join("; ");
    }
  } catch {
    /* ignore */
  }
  throw new Error(detail);
}

async function authHeaders(explicitToken?: string): Promise<HeadersInit> {
  const headers: Record<string, string> = {};
  const token = explicitToken ?? (tokenProvider ? await tokenProvider() : null);
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function request(
  path: string,
  init?: RequestInit,
  explicitToken?: string,
): Promise<Response> {
  const headers = new Headers(init?.headers || {});
  const auth = await authHeaders(explicitToken);
  Object.entries(auth).forEach(([k, v]) => headers.set(k, v));

  try {
    return await fetch(`${API_BASE}${path}`, { ...init, headers });
  } catch {
    throw new Error(
      `Cannot reach API at ${API_BASE}. Make sure the backend is running (uvicorn on port 8000).`,
    );
  }
}

export async function registerProfile(
  payload: { role: "teacher" | "student"; display_name?: string },
  token: string,
): Promise<UserProfile> {
  const response = await request(
    "/api/auth/register-profile",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
    token,
  );
  if (!response.ok) await parseError(response);
  return response.json();
}

export async function fetchMe(token?: string): Promise<UserProfile> {
  const response = await request("/api/auth/me", undefined, token);
  if (!response.ok) await parseError(response);
  return response.json();
}

export async function listTextbooks(): Promise<Textbook[]> {
  const response = await request("/api/textbooks");
  if (!response.ok) await parseError(response);
  return response.json();
}

export async function getTextbookQuota(): Promise<{
  used: number;
  max: number;
  remaining: number;
}> {
  const response = await request("/api/textbooks/quota");
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

export async function listMyEvaluations(): Promise<EvaluationRecord[]> {
  const response = await request("/api/evaluations/me");
  if (!response.ok) await parseError(response);
  return response.json();
}

export async function listTextbookEvaluations(
  textbookId: string,
): Promise<EvaluationRecord[]> {
  const response = await request(`/api/evaluations/textbook/${textbookId}`);
  if (!response.ok) await parseError(response);
  return response.json();
}
