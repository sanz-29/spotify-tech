import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { Empty } from "../components/CatalogCard";
import { PageHeading } from "./Songs";
export default function Genres() { const [items, setItems] = useState([]); useEffect(() => { api.genres("?limit=100").then(setItems).catch(() => {}); }, []); return <div className="page"><PageHeading eyebrow="DISCOVER" title="Genres" subtitle="Follow the feeling, not the label." />{items.length ? <div className="genre-grid">{items.map((g, i) => <Link className={`genre-card genre-${i % 5}`} to={`/songs?genre_id=${g.genre_id}`} key={g.genre_id}><span>✦</span><strong>{g.name}</strong></Link>)}</div> : <Empty>No genres found.</Empty>}</div>; }
