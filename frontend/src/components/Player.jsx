import { useEffect, useRef, useState } from "react";
import { usePlayer } from "../context/PlayerContext";
import { API_URL } from "../api/client";

export default function Player() {
  const { current, setCurrent } = usePlayer();
  const audio = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [volume, setVolume] = useState(0.8);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!current || !audio.current) return;
    audio.current.load();
    audio.current.play().then(() => setPlaying(true)).catch(() => setPlaying(false));
  }, [current]);
  if (!current) return null;

  const toggle = () => {
    if (playing) audio.current.pause();
    else audio.current.play().catch(() => setPlaying(false));
  };
  return <footer className="player">
    <div className="player-track"><div className="mini-cover">{current.cover_image_url ? <img src={current.cover_image_url} alt="" /> : "♪"}</div><div><strong>{current.title}</strong><span>Artist #{current.artist_id}</span></div></div>
    <div className="player-center"><div className="player-buttons"><button aria-label="Previous">◀◀</button><button className="play-control" onClick={toggle}>{playing ? "❚❚" : "▶"}</button><button aria-label="Next">▶▶</button></div><input aria-label="Playback progress" type="range" min="0" max="100" value={progress} onChange={(e) => { setProgress(e.target.value); if (audio.current?.duration) audio.current.currentTime = (e.target.value / 100) * audio.current.duration; }} /></div>
    <div className="volume"><span>♬</span><input aria-label="Volume" type="range" min="0" max="1" step="0.05" value={volume} onChange={(e) => { setVolume(e.target.value); audio.current.volume = e.target.value; }} /></div>
    <audio ref={audio} src={current.audio_url?.startsWith("http") ? current.audio_url : `${API_URL}${current.audio_url || ""}`} onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onTimeUpdate={(e) => setProgress(e.currentTarget.duration ? (e.currentTarget.currentTime / e.currentTarget.duration) * 100 : 0)} onEnded={() => setCurrent(null)} />
  </footer>;
}
