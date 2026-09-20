import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Player from "./Player";

export default function Layout() {
  const { user, logout } = useAuth();
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <NavLink className="brand" to="/"><span className="brand-mark">♪</span> Spotify Tech</NavLink>
        <nav>
          <NavLink to="/" end>⌂ <span>Home</span></NavLink>
          <NavLink to="/songs">♫ <span>Songs</span></NavLink>
          <NavLink to="/artists">◉ <span>Artists</span></NavLink>
          <NavLink to="/albums">▣ <span>Albums</span></NavLink>
          <NavLink to="/genres">✦ <span>Genres</span></NavLink>
          <NavLink to="/playlists">▤ <span>Playlists</span></NavLink>
          {["artist", "admin"].includes(user?.role) && <NavLink to="/artist/manage">✎ <span>Artist studio</span></NavLink>}
          {user?.role === "admin" && <NavLink to="/admin">◆ <span>Admin</span></NavLink>}
        </nav>
        <div className="sidebar-footer">
          <div className="user-chip"><span className="avatar">{user?.username?.[0]?.toUpperCase()}</span><span><strong>{user?.username}</strong><small>{user?.role}</small></span></div>
          <button className="ghost-button" onClick={logout}>Log out</button>
        </div>
      </aside>
      <main className="main-area"><Outlet /></main>
      <Player />
    </div>
  );
}
