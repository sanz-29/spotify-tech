import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth(); const navigate = useNavigate(); const location = useLocation();
  const [form, setForm] = useState({ username: "", password: "" }); const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  async function submit(e) { e.preventDefault(); setBusy(true); setError(""); try { await login(form); navigate(location.state?.from?.pathname || "/dashboard", { replace: true }); } catch (err) { setError(err.message); } finally { setBusy(false); } }
  return <AuthScreen title="Welcome back" subtitle="Sign in to continue your listening session."><form className="auth-form" onSubmit={submit}><Field label="Username" value={form.username} onChange={(v) => setForm({ ...form, username: v })} /><Field label="Password" type="password" value={form.password} onChange={(v) => setForm({ ...form, password: v })} />{error && <div className="error-message">{error}</div>}<button className="primary-button wide" disabled={busy}>{busy ? "Signing in..." : "Sign in"}</button></form><p className="auth-switch">New here? <Link to="/register">Create an account</Link></p></AuthScreen>;
}
export function Field({ label, type = "text", value, onChange, placeholder }) { return <label className="field"><span>{label}</span><input required type={type} value={value} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} /></label>; }
export function AuthScreen({ title, subtitle, children }) { return <div className="auth-page"><div className="auth-decoration"><span className="orb orb-one" /><span className="orb orb-two" /><div><span className="brand-mark">♪</span><h1>Spotify Tech</h1><p>A focused home for the music you love.</p></div></div><section className="auth-panel"><Link to="/" className="brand mobile-brand"><span className="brand-mark">♪</span> Spotify Tech</Link><div className="auth-copy"><p className="eyebrow">YOUR SOUND. YOUR SPACE.</p><h2>{title}</h2><p>{subtitle}</p></div>{children}</section></div>; }
