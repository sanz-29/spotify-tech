import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import { SongRow, Empty } from "../components/CatalogCard";

export default function Songs() {
  const [params] = useSearchParams(); const [songs, setSongs] = useState([]); const [q, setQ] = useState(""); const [filters, setFilters] = useState({ artist_id: params.get("artist_id") || "", album_id: params.get("album_id") || "", genre_id: params.get("genre_id") || "" }); const [genres, setGenres] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  useEffect(() => { api.genres("?limit=100").then(setGenres).catch(() => {}); }, []);
  useEffect(() => { setLoading(true); const timer = setTimeout(() => { const action = q.trim() ? api.searchSongs(q.trim()) : api.songs(`?limit=100${Object.entries(filters).filter(([, v]) => v).map(([k, v]) => `&${k}=${v}`).join("")}`); action.then(setSongs).catch((e) => setError(e.message)).finally(() => setLoading(false)); }, 250); return () => clearTimeout(timer); }, [q, filters]);
  return <div className="page"><PageHeading eyebrow="LIBRARY" title="Songs" subtitle="Browse everything in the catalogue." /><div className="toolbar"><label className="search-input">⌕<input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search title, artist, album or genre" /></label><select value={filters.genre_id} onChange={(e) => setFilters({ ...filters, genre_id: e.target.value })}><option value="">All genres</option>{genres.map((g) => <option key={g.genre_id} value={g.genre_id}>{g.name}</option>)}</select></div>{loading ? <div className="center-state">Loading songs...</div> : error ? <div className="error-message">{error}</div> : songs.length ? <div className="song-list">{songs.map((song) => <SongRow key={song.song_id} song={song} />)}</div> : <Empty>No songs match that search.</Empty>}</div>;
}
export function PageHeading({ eyebrow, title, subtitle }) { return <header className="page-heading"><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{subtitle}</p></header>; }
