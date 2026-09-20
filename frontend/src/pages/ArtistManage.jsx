import { useEffect, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { Field } from "./Login";
import { PageHeading } from "./Songs";

export default function ArtistManage() {
  const { user } = useAuth(); const [artist, setArtist] = useState(null); const [form, setForm] = useState({ name: "", bio: "", image_url: "" }); const [error, setError] = useState(""); const [message, setMessage] = useState("");
  useEffect(() => { api.myArtist().then((match) => { setArtist(match); setForm({ name: match.name, bio: match.bio || "", image_url: match.image_url || "" }); }).catch((e) => { if (!e.message.toLowerCase().includes("not found")) setError(e.message); }); }, [user.user_id]);
  async function submit(e) { e.preventDefault(); try { const result = artist ? await api.updateArtist(artist.artist_id, form) : await api.createArtist(form); setArtist(result); setMessage("Profile saved."); } catch (e) { setError(e.message); } }
  return <div className="page"><PageHeading eyebrow="ARTIST STUDIO" title="Your artist profile" subtitle="Manage the public profile attached to your artist account." />{error && <div className="error-message">{error}</div>}{message && <div className="success-message">{message}</div>}<form className="panel form-panel" onSubmit={submit}><Field label="Artist name" value={form.name} onChange={(v) => setForm({ ...form, name: v })} /><label className="field"><span>Biography</span><textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} /></label><Field label="Profile image URL" value={form.image_url} onChange={(v) => setForm({ ...form, image_url: v })} /><button className="primary-button">{artist ? "Save changes" : "Create profile"}</button></form></div>;
}
