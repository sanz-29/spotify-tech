import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import { AlbumCard, Empty, SongRow } from "../components/CatalogCard";

export default function ArtistProfile() {
  const { id } = useParams(); const [artist, setArtist] = useState(null); const [songs, setSongs] = useState([]); const [albums, setAlbums] = useState([]); const [error, setError] = useState("");
  useEffect(() => { Promise.all([api.artist(id), api.songs(`?artist_id=${id}&limit=100`), api.albums(`?limit=100`)]).then(([a, s, al]) => { setArtist(a); setSongs(s); setAlbums(al.filter((x) => x.artist_id === Number(id))); }).catch((e) => setError(e.message)); }, [id]);
  if (error) return <div className="page"><div className="error-message">{error}</div></div>;
  if (!artist) return <div className="center-state">Loading artist...</div>;
  return <div className="page"><div className="profile-hero"><div className="profile-image">{artist.image_url ? <img src={artist.image_url} alt="" /> : "◉"}</div><div><p className="eyebrow">ARTIST PROFILE</p><h1>{artist.name}</h1><p>{artist.bio || "No biography yet."}</p></div></div><div className="section-title"><h2>Top songs</h2></div>{songs.length ? <div className="song-list">{songs.map((s) => <SongRow key={s.song_id} song={s} />)}</div> : <Empty>No songs yet.</Empty>}<div className="section-title"><h2>Albums</h2></div><div className="entity-grid">{albums.map((a) => <AlbumCard key={a.album_id} album={a} />)}</div></div>;
}
