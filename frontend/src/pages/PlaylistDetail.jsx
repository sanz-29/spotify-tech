import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../api/client";
import { Empty, SongRow } from "../components/CatalogCard";
import { PageHeading } from "./Songs";

export default function PlaylistDetail() {
  const { id } = useParams(); const navigate = useNavigate(); const [playlist, setPlaylist] = useState(null); const [songs, setSongs] = useState([]); const [allSongs, setAllSongs] = useState([]); const [selected, setSelected] = useState(""); const [form, setForm] = useState({ name: "", description: "" }); const [error, setError] = useState(""); const [message, setMessage] = useState("");
  const load = () => Promise.all([api.playlists(id), api.playlistSongs(id)]).then(([p, s]) => { setPlaylist(p); setSongs(s); }).catch((e) => setError(e.message));
  useEffect(() => { load(); api.songs("?limit=100").then(setAllSongs).catch((e) => setError(e.message)); }, [id]);
  useEffect(() => { if (playlist) setForm({ name: playlist.name, description: playlist.description || "" }); }, [playlist]);
  async function add() { if (!selected) return; try { await api.addPlaylistSong(id, Number(selected)); setSelected(""); load(); } catch (e) { setError(e.message); } }
  async function remove(songId) { try { await api.removePlaylistSong(id, songId); load(); } catch (e) { setError(e.message); } }
  async function update(e) { e.preventDefault(); try { const updated = await api.updatePlaylist(id, form); setPlaylist(updated); setMessage("Playlist updated."); setError(""); } catch (e) { setError(e.message); } }
  if (error && !playlist) return <div className="page"><div className="error-message">{error}</div><button className="text-button" onClick={() => navigate("/playlists")}>Back to playlists</button></div>;
  if (!playlist) return <div className="center-state">Loading playlist...</div>;
  return <div className="page"><PageHeading eyebrow="PLAYLIST" title={playlist.name} subtitle={playlist.description || "A personal collection."} /><form className="panel compact-form" onSubmit={update}><input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} aria-label="Playlist name" /><textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} aria-label="Playlist description" /><button className="primary-button">Save playlist</button></form><div className="playlist-actions"><select value={selected} onChange={(e) => setSelected(e.target.value)}><option value="">Add a song...</option>{allSongs.filter((s) => !songs.some((x) => x.song_id === s.song_id)).map((s) => <option key={s.song_id} value={s.song_id}>{s.title}</option>)}</select><button className="primary-button" onClick={add}>Add song</button></div>{message && <div className="success-message">{message}</div>}{error && <div className="error-message">{error}</div>}{songs.length ? <div className="song-list">{songs.map((song) => <SongRow key={song.song_id} song={song} onAdd={() => remove(song.song_id)} />)}</div> : <Empty>Add songs from the catalogue to get started.</Empty>}</div>;
}
