# Spotify Tech API

Spotify Tech API is a FastAPI music catalog and playlist service backed by
MySQL and SQLAlchemy. It provides public catalog reads, authenticated
playlist management, artist-owned catalog management, and administrator CRUD
operations.

## Features

- User registration and Argon2 password hashing
- JWT bearer authentication with expiration
- `user`, `artist`, and `admin` roles
- Owner checks for artist profiles, albums, songs, and playlists
- Artist, album, song, genre, and playlist CRUD
- Playlist/song association management
- Paginated catalog and administrator list endpoints
- Safe validation and consistent conflict/database error responses
- OpenAPI documentation at `/docs` and `/redoc`
- Static audio delivery from `/music`
- SQLite-compatible test suite that does not require a live MySQL server

## Architecture

```text
main.py
  └── app/app.py
      ├── app/api/          FastAPI routers
      ├── app/models/       SQLAlchemy models and relationships
      ├── app/schemas/      Pydantic request/response models
      ├── app/auth.py       JWT creation and verification
      ├── app/security.py   Argon2 password helpers
      ├── app/dependencies.py  authentication and RBAC dependencies
      └── app/database.py   SQLAlchemy engine and sessions
```

## Tech stack

- Python 3.11+
- FastAPI and Uvicorn
- MySQL with PyMySQL
- SQLAlchemy 2.x
- Pydantic 2.x
- Argon2 and `python-jose`
- pytest and FastAPI `TestClient`

## Database structure

The core relationships are:

- A user owns playlists.
- An artist may be linked to one artist-role user.
- An artist has albums and songs.
- An album belongs to an artist and can contain songs.
- A song can reference an artist, album, and genre.
- `playlist_songs` is a unique many-to-many association between playlists and
  songs.

Playlist and playlist-song associations are cleaned up through the existing
ORM/database cascade configuration. Artist, album, genre, and song deletes
retain referential integrity rather than silently deleting unrelated catalog
data.

See [docs/database_schema.sql](docs/database_schema.sql) for the SQL
reference schema.

## Authentication and authorization

Register with `POST /users/`, then log in with `POST /users/login`:

```json
{
  "username": "listener",
  "email": "listener@example.com",
  "password": "password123"
}
```

The login response includes `access_token` and `token_type: "bearer"`.
Send the token on protected requests:

```text
Authorization: Bearer <access_token>
```

`GET /users/me` validates the token, loads the current database user, and
never returns the stored password hash. Admin routes use the reusable
`require_admin` dependency and return `403` for non-admin users. Artist-owned
resources are checked against the authenticated artist before update or
delete operations.

## API endpoints

### Health

- `GET /`
- `GET /health`

### Users

- `POST /users/`
- `POST /users/login`
- `GET /users/me`

### Public catalog and artist management

- `GET|POST /artists/`
- `GET /artists/search`
- `GET /artists/me`
- `GET|PUT|DELETE /artists/{artist_id}`
- `GET|POST /albums/`
- `GET /albums/search`
- `GET|PUT|DELETE /albums/{album_id}`
- `GET|POST /songs/`
- `GET /songs/search`
- `GET|PUT|DELETE /songs/{song_id}`
- `GET|POST /genres/`
- `GET|PUT|DELETE /genres/{genre_id}`

Create/update catalog operations require the appropriate artist or admin
role. Genre writes are administrator-only.

### Playlists

- `GET|POST /playlists/`
- `GET|PUT|DELETE /playlists/{playlist_id}`
- `POST|GET /playlists/{playlist_id}/songs`
- `DELETE /playlists/{playlist_id}/songs/{song_id}`

Playlist endpoints require authentication and only expose the current user's
playlists.

### Admin

- `GET|PUT|DELETE /admin/users/{user_id}`
- `GET /admin/users`
- `GET|PUT|DELETE /admin/artists/{artist_id}`
- `GET /admin/artists`
- `GET|PUT|DELETE /admin/albums/{album_id}`
- `GET /admin/albums`
- `GET|PUT|DELETE /admin/songs/{song_id}`
- `GET /admin/songs`
- `GET|POST|PUT|DELETE /admin/genres`

Every `/admin/*` endpoint requires an authenticated user with role `admin`.

## Local setup

From the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with a real MySQL connection string and a long random secret.
Never commit `.env`.

For a local MySQL database, create the database named in `DATABASE_URL` and
ensure the configured user can create and alter application tables.

## Run the server

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

The same entrypoint is suitable for deployment platforms. On platforms that
provide a `PORT` variable, use:

```text
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The application also exposes `/music` for files in the repository's `music`
directory.

## Environment variables

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | SQLAlchemy URL, for example `mysql+pymysql://...` |
| `SECRET_KEY` | Yes | Long random JWT signing secret |
| `ALGORITHM` | No | JWT algorithm; defaults to `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Positive token lifetime; defaults to `30` |
| `ALLOWED_ORIGINS` | No | Comma-separated browser origins |

See [.env.example](.env.example) for placeholders only.

## Tests

The suite uses an isolated SQLite database and exercises the real FastAPI
application:

```powershell
pytest
```

Coverage includes registration and login, missing/invalid/expired JWTs,
admin RBAC, artist and playlist ownership boundaries, and playlist/song
relationships.

## Swagger documentation

With the server running:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

Use the **Authorize** control in Swagger UI with a bearer token.

## Deployment checklist

- Set `DATABASE_URL`, `SECRET_KEY`, and allowed browser origins in the
  deployment environment.
- Use a managed MySQL database with backups and restricted credentials.
- Run the application with `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- Put TLS termination and rate limiting at the platform or reverse proxy.
- Do not expose `.env`, database credentials, or JWT secrets in logs.
- Apply schema changes through a migration process before changing existing
  production tables.

## Security notes

Passwords are never stored or returned in plaintext. Missing, invalid, or
expired bearer tokens return `401`; authenticated users without the required
role return `403`. SQLAlchemy query parameters are used for user input, and
public list/search endpoints have bounded pagination or result limits.
