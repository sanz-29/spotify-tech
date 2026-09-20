import { useEffect, useState, useRef } from "react";
import { api, API_URL } from "./api/client";

function Dashboard() {
  const [songs, setSongs] = useState([]);
  const [currentSong, setCurrentSong] = useState(null);
  const [search, setSearch] = useState("");
  const [isPlaying, setIsPlaying] = useState(false);

  const audioRef = useRef(null);

  useEffect(() => {
    api.songs()
      .then(setSongs)
      .catch((error) => {
        console.error("Error fetching songs:", error);
      });
  }, []);

  const filteredSongs = songs.filter((song) =>
    song.title.toLowerCase().includes(search.toLowerCase())
  );

  const playSong = (song) => {
    setCurrentSong(song);
    setIsPlaying(true);
  };

  const togglePlayPause = () => {
    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  return (
    <div className="dashboard">

      {/* Sidebar */}
      <aside className="sidebar">
        <h1 className="logo">Spotify Tech</h1>

        <nav>
          <button>🏠 Home</button>
          <button>🔍 Search</button>
          <button>❤️ Favorites</button>
          <button>📂 Playlists</button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">

        <div className="top-section">
          <h2>Good Morning 👋</h2>

          <input
            className="search"
            type="text"
            placeholder="Search songs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <h2>All Songs</h2>

        <div className="song-grid">

          {filteredSongs.map((song) => (
            <div className="song-card" key={song.song_id}>

              <div className="album-cover">
                🎵
              </div>

              <h3>{song.title}</h3>

              <p>Artist #{song.artist_id}</p>

              <button
                className="play-button"
                onClick={() => playSong(song)}
              >
                ▶
              </button>

            </div>
          ))}

        </div>

        {filteredSongs.length === 0 && (
          <p className="no-songs">
            No songs found 🎵
          </p>
        )}

      </main>

      {/* Bottom Player */}
      {currentSong && (
        <div className="music-player">

          <div className="player-song-info">

            <div className="player-cover">
              🎵
            </div>

            <div>
              <strong>{currentSong.title}</strong>

              <p>
                Artist #{currentSong.artist_id}
              </p>
            </div>

          </div>

          <div className="player-controls">

            <button>⏮</button>

            <button
              className="main-play-button"
              onClick={togglePlayPause}
            >
              {isPlaying ? "⏸" : "▶"}
            </button>

            <button>⏭</button>

          </div>

          <audio
            ref={audioRef}
            src={
              currentSong.audio_url?.startsWith("http")
                ? currentSong.audio_url
                : `${API_URL}${currentSong.audio_url || ""}`
            }
            autoPlay
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
          />

        </div>
      )}

    </div>
  );
}

export default Dashboard;