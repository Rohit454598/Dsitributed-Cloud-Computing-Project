import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
  type User,
} from "firebase/auth";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { fetchMe, registerProfile, type UserProfile } from "../api/client";
import { auth, firebaseReady } from "../lib/firebase";

type AuthContextValue = {
  firebaseReady: boolean;
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  getIdToken: () => Promise<string | null>;
  login: (email: string, password: string) => Promise<void>;
  signup: (
    email: string,
    password: string,
    role: "teacher" | "student",
    displayName: string,
  ) => Promise<void>;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshProfile = useCallback(async () => {
    if (!user) {
      setProfile(null);
      return;
    }
    try {
      const me = await fetchMe();
      setProfile(me);
    } catch {
      setProfile(null);
    }
  }, [user]);

  useEffect(() => {
    if (!auth) {
      setLoading(false);
      return;
    }
    return onAuthStateChanged(auth, async (next) => {
      setUser(next);
      setLoading(false);
    });
  }, []);

  useEffect(() => {
    if (!user) {
      setProfile(null);
      return;
    }
    void refreshProfile();
  }, [user, refreshProfile]);

  const getIdToken = useCallback(async () => {
    if (!user) return null;
    return user.getIdToken();
  }, [user]);

  const login = useCallback(async (email: string, password: string) => {
    if (!auth) throw new Error("Firebase is not configured. Add VITE_FIREBASE_* to frontend/.env");
    await signInWithEmailAndPassword(auth, email, password);
  }, []);

  const signup = useCallback(
    async (
      email: string,
      password: string,
      role: "teacher" | "student",
      displayName: string,
    ) => {
      if (!auth) throw new Error("Firebase is not configured. Add VITE_FIREBASE_* to frontend/.env");
      const cred = await createUserWithEmailAndPassword(auth, email, password);
      await registerProfile(
        { role, display_name: displayName },
        await cred.user.getIdToken(),
      );
      const me = await fetchMe(await cred.user.getIdToken());
      setProfile(me);
    },
    [],
  );

  const logout = useCallback(async () => {
    if (!auth) return;
    await signOut(auth);
    setProfile(null);
  }, []);

  const value = useMemo(
    () => ({
      firebaseReady,
      user,
      profile,
      loading,
      getIdToken,
      login,
      signup,
      logout,
      refreshProfile,
    }),
    [user, profile, loading, getIdToken, login, signup, logout, refreshProfile],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
