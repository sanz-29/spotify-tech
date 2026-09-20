import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { PlayerProvider } from "./context/PlayerContext";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import Songs from "./pages/Songs";
import Artists from "./pages/Artists";
import ArtistProfile from "./pages/ArtistProfile";
import ArtistManage from "./pages/ArtistManage";
import Albums from "./pages/Albums";
import Genres from "./pages/Genres";
import Playlists from "./pages/Playlists";
import PlaylistDetail from "./pages/PlaylistDetail";
import Admin from "./pages/Admin";

function AppRoutes() {
  const { user, loading } = useAuth();
  return <Routes>
    <Route
      path="/"
      element={
        loading
          ? <div className="center-state">Loading your library...</div>
          : user
            ? <Navigate to="/dashboard" replace />
            : <Login />
      }
    />
    <Route path="/login" element={user ? <Navigate to="/dashboard" replace /> : <Login />} />
    <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <Register />} />
    <Route element={<ProtectedRoute />}><Route element={<Layout />}>
      <Route path="/dashboard" element={<Home />} /><Route path="/songs" element={<Songs />} /><Route path="/artists" element={<Artists />} /><Route path="/artists/:id" element={<ArtistProfile />} /><Route path="/albums" element={<Albums />} /><Route path="/genres" element={<Genres />} /><Route path="/playlists" element={<Playlists />} /><Route path="/playlists/:id" element={<PlaylistDetail />} />
      <Route element={<ProtectedRoute roles={["artist", "admin"]} />}><Route path="/artist/manage" element={<ArtistManage />} /></Route>
      <Route element={<ProtectedRoute roles={["admin"]} />}><Route path="/admin" element={<Admin />} /></Route>
    </Route></Route>
    <Route path="*" element={<Navigate to={user ? "/dashboard" : "/"} replace />} />
  </Routes>;
}
export default function App() { return <BrowserRouter><AuthProvider><PlayerProvider><AppRoutes /></PlayerProvider></AuthProvider></BrowserRouter>; }
