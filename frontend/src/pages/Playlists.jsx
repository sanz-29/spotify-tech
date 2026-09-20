import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { Empty } from "../components/CatalogCard";
import { PageHeading } from "./Songs";

export default function Playlists() {
  const [items, setItems] = useState([]); const [form, setForm] = useState({ name: "", description: "" }); const [error, setError] = useState("");
  const load = () => api.playlists("?limit=100").then(setItems).catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, []);
  async function create(e) { e.preventDefault(); try { await api.createPlaylist(form); setForm({ name: "", description: "" }); load(); } catch (e) { setError(e.message); } }
  async function remove(id) { if (!window.confirm("Delete this playlist?")) return; try { await api.deletePlaylist(id); load(); } catch (e) { setError(e.message); } }
  return <div className="page"><PageHeading eyebrow="YOUR LIBRARY" title="Playlists" subtitle="Curate a space for every mood." /><div className="split-layout"><form className="panel compact-form" onSubmit={create}><h3>Create a playlist</h3><input required placeholder="Playlist name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /><textarea placeholder="Description (optional)" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /><button className="primary-button">Create playlist</button></form><div>{error && <div className="error-message">{error}</div>}{items.length ? <div className="playlist-grid">{items.map((p) => <div className="playlist-card" key={p.playlist_id}><Link to={`/playlists/${p.playlist_id}`}><div className="playlist-art">♫</div><strong>{p.name}</strong><span>{p.description || "No description"}</span></Link><button className="text-button danger" onClick={() => remove(p.playlist_id)}>Delete</button></div>)}</div> : <Empty>Create your first playlist.</Empty>}</div></div></div>;
}
