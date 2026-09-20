import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api, TOKEN_KEY } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem(TOKEN_KEY)));

  useEffect(() => {
    const expire = () => logout();
    window.addEventListener("spotify-auth-expired", expire);
    if (localStorage.getItem(TOKEN_KEY)) {
      api.me().then(setUser).catch(logout).finally(() => setLoading(false));
    }
    return () => window.removeEventListener("spotify-auth-expired", expire);
  }, []);

  async function login(credentials) {
    const data = await api.login(credentials);
    localStorage.setItem(TOKEN_KEY, data.access_token);
    const currentUser = await api.me();
    setUser(currentUser);
    return currentUser;
  }

  async function register(values) {
    await api.register(values);
    return login({ username: values.username, password: values.password });
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    setUser(null);
    setLoading(false);
  }

  const value = useMemo(() => ({ user, loading, login, register, logout }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
