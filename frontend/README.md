# Spotify Tech frontend

This React/Vite frontend uses the existing FastAPI API.

## Run locally

```powershell
cd K:\capstone\spotify-tech\frontend
npm install
npm run dev
```

The backend should be running at `http://127.0.0.1:8000`. Override it with:

```env
VITE_API_URL=http://127.0.0.1:8000
```

The frontend stores the access token in `localStorage` under
`spotify_tech_token`, sends it as a Bearer token, and clears it when the API
returns `401`.
