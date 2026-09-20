import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { AuthScreen, Field } from "./Login";

export default function Register() {
  const { register } = useAuth(); const navigate = useNavigate(); const [form, setForm] = useState({ username: "", email: "", password: "" }); const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  async function submit(e) { e.preventDefault(); setBusy(true); setError(""); try { await register(form); navigate("/dashboard"); } catch (err) { setError(err.message); } finally { setBusy(false); } }
  return <AuthScreen title="Make it yours" subtitle="Create your account and start building your library."><form className="auth-form" onSubmit={submit}><Field label="Username" value={form.username} onChange={(v) => setForm({ ...form, username: v })} /><Field label="Email" type="email" value={form.email} onChange={(v) => setForm({ ...form, email: v })} /><Field label="Password" type="password" value={form.password} onChange={(v) => setForm({ ...form, password: v })} />{error && <div className="error-message">{error}</div>}<button className="primary-button wide" disabled={busy}>{busy ? "Creating account..." : "Create account"}</button></form><p className="auth-switch">Already have an account? <Link to="/login">Sign in</Link></p></AuthScreen>;
}
