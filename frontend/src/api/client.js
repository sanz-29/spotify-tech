const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const TOKEN_KEY = "spotify_tech_token";

function formatValidationErrors(detail) {
  if (!Array.isArray(detail)) return detail;
  return detail
    .map((item) => {
      const location = Array.isArray(item.loc) ? item.loc.join(".") : "request";
      return `${location}: ${item.msg}`;
    })
    .join("; ");
}

export async function request(path, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  const headers = new Headers(options.headers || {});

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (response.status === 401) {
    window.dispatchEvent(new Event("spotify-auth-expired"));
  }
  if (!response.ok) {
    const detail = formatValidationErrors(data?.detail);
    throw new Error(detail || data?.message || `Request failed (${response.status})`);
  }
  return data;
}

const json = (method, body) => ({
  method,
  body: JSON.stringify(body),
});

export const api = {
  auth: {
    register: (body) => request("/users/", json("POST", body)),
    login: (body) => request("/users/login", json("POST", body)),
    getCurrentUser: () => request("/users/me"),
  },
  artists: {
    list: (params = "") => request(`/artists/${params}`),
    get: (id) => request(`/artists/${id}`),
    search: (query) => request(`/artists/search?q=${encodeURIComponent(query)}`),
    me: () => request("/artists/me"),
    create: (body) => request("/artists/", json("POST", body)),
    update: (id, body) => request(`/artists/${id}`, json("PUT", body)),
    remove: (id) => request(`/artists/${id}`, { method: "DELETE" }),
  },
  albums: {
    list: (params = "") => request(`/albums/${params}`),
    get: (id) => request(`/albums/${id}`),
    search: (query) => request(`/albums/search?q=${encodeURIComponent(query)}`),
    create: (body) => request("/albums/", json("POST", body)),
    update: (id, body) => request(`/albums/${id}`, json("PUT", body)),
    remove: (id) => request(`/albums/${id}`, { method: "DELETE" }),
  },
  songs: {
    list: (params = "") => request(`/songs/${params}`),
    get: (id) => request(`/songs/${id}`),
    search: (query) => request(`/songs/search?q=${encodeURIComponent(query)}`),
    create: (body) => request("/songs/", json("POST", body)),
    update: (id, body) => request(`/songs/${id}`, json("PUT", body)),
    remove: (id) => request(`/songs/${id}`, { method: "DELETE" }),
  },
  genres: {
    list: (params = "") => request(`/genres/${params}`),
    get: (id) => request(`/genres/${id}`),
    create: (body) => request("/genres/", json("POST", body)),
    update: (id, body) => request(`/genres/${id}`, json("PUT", body)),
    remove: (id) => request(`/genres/${id}`, { method: "DELETE" }),
  },
  playlists: {
    list: (params = "") => request(`/playlists/${params}`),
    get: (id) => request(`/playlists/${id}`),
    create: (body) => request("/playlists/", json("POST", body)),
    update: (id, body) => request(`/playlists/${id}`, json("PUT", body)),
    remove: (id) => request(`/playlists/${id}`, { method: "DELETE" }),
    addSong: (id, songId) => request(`/playlists/${id}/songs`, json("POST", { song_id: songId })),
    songs: (id) => request(`/playlists/${id}/songs`),
    removeSong: (id, songId) => request(`/playlists/${id}/songs/${songId}`, { method: "DELETE" }),
  },
  admin: {
    users: () => request("/admin/users"),
    updateUser: (id, body) => request(`/admin/users/${id}`, json("PUT", body)),
    deleteUser: (id) => request(`/admin/users/${id}`, { method: "DELETE" }),
    artists: () => request("/admin/artists"),
    updateArtist: (id, body) => request(`/admin/artists/${id}`, json("PUT", body)),
    deleteArtist: (id) => request(`/admin/artists/${id}`, { method: "DELETE" }),
    songs: () => request("/admin/songs"),
    deleteSong: (id) => request(`/admin/songs/${id}`, { method: "DELETE" }),
    albums: () => request("/admin/albums"),
    deleteAlbum: (id) => request(`/admin/albums/${id}`, { method: "DELETE" }),
    genres: () => request("/admin/genres"),
    createGenre: (body) => request("/admin/genres", json("POST", body)),
    updateGenre: (id, body) => request(`/admin/genres/${id}`, json("PUT", body)),
    deleteGenre: (id) => request(`/admin/genres/${id}`, { method: "DELETE" }),
  },
};

// Keep the compact names used by the existing pages while exposing the
// namespaced API above for new integrations.
api.login = api.auth.login;
api.register = api.auth.register;
api.me = api.auth.getCurrentUser;
api.artists = Object.assign(api.artists.list, api.artists);
api.albums = Object.assign(api.albums.list, api.albums);
api.songs = Object.assign(api.songs.list, api.songs);
api.genres = Object.assign(api.genres.list, api.genres);
api.playlists = Object.assign(api.playlists.list, api.playlists);
api.searchArtists = api.artists.search;
api.searchAlbums = api.albums.search;
api.searchSongs = api.songs.search;
api.artist = api.artists.get;
api.myArtist = api.artists.me;
api.createArtist = api.artists.create;
api.updateArtist = api.artists.update;
api.deleteArtist = api.artists.remove;
api.createPlaylist = api.playlists.create;
api.updatePlaylist = api.playlists.update;
api.deletePlaylist = api.playlists.remove;
api.playlistSongs = api.playlists.songs;
api.addPlaylistSong = api.playlists.addSong;
api.removePlaylistSong = api.playlists.removeSong;

export { API_URL, TOKEN_KEY };
