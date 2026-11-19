import { useState, type FormEvent } from "react";
import { useAuth } from "../auth/AuthContext";
import { registerProfile } from "../api/client";

type Props = {
  mode?: "login" | "signup" | "complete-profile";
};

export function AuthForm({ mode: initialMode = "login" }: Props) {
  const { firebaseReady, login, signup, getIdToken, refreshProfile, logout } = useAuth();
  const [mode, setMode] = useState<"login" | "signup" | "complete-profile">(initialMode);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [role, setRole] = useState<"teacher" | "student">("student");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (mode === "login") {
        await login(email.trim(), password);
      } else if (mode === "signup") {
        await signup(email.trim(), password, role, displayName.trim());
      } else {
        const token = await getIdToken();
        if (!token) throw new Error("Not signed in.");
        await registerProfile({ role, display_name: displayName.trim() }, token);
        await refreshProfile();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  }

  if (!firebaseReady) {
    return (
      <section className="panel auth-panel">
        <h2>Firebase not configured</h2>
        <p className="muted">
          Copy <code>frontend/.env.example</code> to <code>frontend/.env</code> and add your
          Firebase web keys, then restart the Vite server.
        </p>
      </section>
    );
  }

  return (
    <section className="panel auth-panel">
      <div className="panel-head">
        <h2>
          {mode === "login"
            ? "Sign in"
            : mode === "signup"
              ? "Create account"
              : "Choose your role"}
        </h2>
        <p>
          {mode === "login"
            ? "Use your Firebase email and password."
            : mode === "signup"
              ? "Choose teacher or student during signup."
              : "Save teacher or student role to finish setup."}
        </p>
      </div>

      <form className="auth-form" onSubmit={onSubmit}>
        {(mode === "signup" || mode === "complete-profile") && (
          <>
            <label className="field">
              <span>Display name</span>
              <input
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Optional"
              />
            </label>
            <label className="field">
              <span>Role</span>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value as "teacher" | "student")}
              >
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
              </select>
            </label>
          </>
        )}

        {mode !== "complete-profile" && (
          <>
            <label className="field">
              <span>Email</span>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@school.edu"
              />
            </label>

            <label className="field">
              <span>Password</span>
              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 6 characters"
              />
            </label>
          </>
        )}

        {error && <p className="error">{error}</p>}

        <button type="submit" className="primary" disabled={loading}>
          {loading
            ? "Please wait…"
            : mode === "login"
              ? "Sign in"
              : mode === "signup"
                ? "Sign up"
                : "Save profile"}
        </button>
      </form>

      {mode !== "complete-profile" ? (
        <button
          type="button"
          className="ghost linkish"
          onClick={() => setMode(mode === "login" ? "signup" : "login")}
        >
          {mode === "login" ? "Need an account? Sign up" : "Already have an account? Sign in"}
        </button>
      ) : (
        <button type="button" className="ghost linkish" onClick={() => void logout()}>
          Sign out
        </button>
      )}
    </section>
  );
}
