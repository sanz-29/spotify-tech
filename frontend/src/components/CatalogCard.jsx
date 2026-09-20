import { Link } from "react-router-dom";
import { usePlayer } from "../context/PlayerContext";

export function SongRow({ song, onAdd }) {
  const { setCurrent } = usePlayer();
  return <div className="song-row"><button className="row-play" onClick={() => setCurrent(song)}>▶</button><div className="row-cover">{song.cover_image_url ? <img src={song.cover_image_url} alt="" /> : "♪"}</div><div className="row-main"><strong>{song.title}</strong><span>Artist #{song.artist_id}</span></div><span className="row-meta">{song.duration ? `${Math.floor(song.duration / 60)}:${String(song.duration % 60).padStart(2, "0")}` : ""}</span>{onAdd && <button className="icon-button" onClick={() => onAdd(song)}>＋</button>}</div>;
}

export function ArtistCard({ artist }) {
  return <Link className="entity-card" to={`/artists/${artist.artist_id}`}><div className="entity-image">{artist.image_url ? <img src={artist.image_url} alt="" /> : "◉"}</div><strong>{artist.name}</strong><span>Artist</span></Link>;
}

export function AlbumCard({ album }) {
  return <div className="entity-card"><div className="entity-image">{album.cover_image_url ? <img src={album.cover_image_url} alt="" /> : "▣"}</div><strong>{album.title}</strong><span>Artist #{album.artist_id || "—"}</span></div>;
}

export function Empty({ children = "Nothing here yet." }) { return <div className="empty-state"><span>◌</span><p>{children}</p></div>; }
