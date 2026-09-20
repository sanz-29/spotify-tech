import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Empty } from "../components/CatalogCard";
import { PageHeading } from "./Songs";

const tabs = ["users", "artists", "songs", "albums", "genres"];
export default function Admin() {
  const [tab, setTab] = useState("users"); const [items, setItems] = useState([]); const [error, setError] = useState(""); const [genreName, setGenreName] = useState("");
  const load = () => api.admin[tab]().then(setItems).catch((e) => setError(e.message));
  useEffect(() => { setError(""); api.admin[tab]().then(setItems).catch((e) => setError(e.message)); }, [tab]);
  async function createGenre(e) { e.preventDefault(); try { await api.admin.createGenre({ name: genreName }); setGenreName(""); load(); } catch (e) { setError(e.message); } }
  async function remove(item) { if (!window.confirm("Delete this item?")) return; try { if (tab === "users") await api.admin.deleteUser(item.user_id); if (tab === "artists") await api.admin.deleteArtist(item.artist_id); if (tab === "songs") await api.admin.deleteSong(item.song_id); if (tab === "albums") await api.admin.deleteAlbum(item.album_id); if (tab === "genres") await api.admin.deleteGenre(item.genre_id); load(); } catch (e) { setError(e.message); } }
  return <div className="page"><PageHeading eyebrow="CONTROL ROOM" title="Admin dashboard" subtitle="Manage the catalogue and community from one place." /><div className="admin-tabs">{tabs.map((name) => <button className={tab === name ? "active" : ""} onClick={() => setTab(name)} key={name}>{name}</button>)}</div>{tab === "genres" && <form className="inline-form" onSubmit={createGenre}><input required value={genreName} onChange={(e) => setGenreName(e.target.value)} placeholder="New genre name" /><button className="primary-button">Add genre</button></form>}{error && <div className="error-message">{error}</div>}{items.length ? <div className="admin-table">{items.map((item) => <div className="admin-row" key={item.user_id || item.artist_id || item.song_id || item.album_id || item.genre_id}><div><strong>{item.username || item.name || item.title}</strong><span>{item.email || item.role || (item.artist_id ? `Artist #${item.artist_id}` : "")}</span></div><button className="text-button danger" onClick={() => remove(item)}>Delete</button></div>)}</div> : <Empty>No records found.</Empty>}</div>;
}
