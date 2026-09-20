import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { SongRow, ArtistCard, AlbumCard, Empty } from "../components/CatalogCard";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { user } = useAuth(); const [songs, setSongs] = useState([]); const [artists, setArtists] = useState([]); const [albums, setAlbums] = useState([]); const [error, setError] = useState("");
  useEffect(() => { Promise.all([api.songs("?limit=8"), api.artists("?limit=6"), api.albums("?limit=6")]).then(([s, a, al]) => { setSongs(s); setArtists(a); setAlbums(al); }).catch((e) => setError(e.message)); }, []);
  return <div className="page"><header className="page-header"><div><p className="eyebrow">GOOD TO SEE YOU</p><h1>Good morning, {user?.username}.</h1></div><Link className="search-pill" to="/songs">⌕ <span>Search your library</span></Link></header>{error && <div className="error-message">{error}</div>}<section className="hero-banner"><div><p className="eyebrow">YOUR DAILY SOUNDTRACK</p><h2>Find something<br /><em>worth replaying.</em></h2><Link className="primary-button" to="/songs">Browse songs <span>→</span></Link></div><div className="hero-art">♪</div></section><SectionTitle title="Fresh in the catalogue" link="/songs" /><div className="song-list">{songs.length ? songs.map((song) => <SongRow key={song.song_id} song={song} />) : <Empty>No songs have been added yet.</Empty>}</div><SectionTitle title="Artists to explore" link="/artists" /><div className="entity-grid">{artists.map((artist) => <ArtistCard key={artist.artist_id} artist={artist} />)}</div><SectionTitle title="Albums" link="/albums" /><div className="entity-grid">{albums.map((album) => <AlbumCard key={album.album_id} album={album} />)}</div></div>;
}
function SectionTitle({ title, link }) { return <div className="section-title"><h2>{title}</h2><Link to={link}>View all →</Link></div>; }
