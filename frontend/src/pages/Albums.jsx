import { useEffect, useState } from "react";
import { api } from "../api/client";
import { AlbumCard, Empty } from "../components/CatalogCard";
import { PageHeading } from "./Songs";
export default function Albums() { const [items, setItems] = useState([]); const [q, setQ] = useState(""); useEffect(() => { const t = setTimeout(() => (q ? api.searchAlbums(q) : api.albums("?limit=100")).then(setItems).catch(() => {}), 250); return () => clearTimeout(t); }, [q]); return <div className="page"><PageHeading eyebrow="DISCOVER" title="Albums" subtitle="A collection of complete worlds in sound." /><label className="search-input wide-search">⌕<input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search albums" /></label>{items.length ? <div className="entity-grid">{items.map((item) => <AlbumCard key={item.album_id} album={item} />)}</div> : <Empty>No albums found.</Empty>}</div>; }
