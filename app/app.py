from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import Base, engine
from app.models import album, artist, genre, playlist, playlist_song, song, user

from app.api.artist import router as artist_router
from app.api.user import router as user_router
from app.api.song import router as song_router
from app.api.album import router as album_router
from app.api.genre import router as genre_router
from app.api.playlist import router as playlist_router
from app.api.admin import router as admin_router


# Create FastAPI application
app = FastAPI(
    title="Spotify Tech API",
    version="1.0.0"
)


@app.exception_handler(IntegrityError)
async def handle_integrity_error(
    request: Request,
    exc: IntegrityError
):
    return JSONResponse(
        status_code=409,
        content={"detail": "The request conflicts with existing data"}
    )


@app.exception_handler(SQLAlchemyError)
async def handle_database_error(
    request: Request,
    exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred"}
    )


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Serve music files
app.mount(
    "/music",
    StaticFiles(directory="music"),
    name="music"
)


# Register API routers
app.include_router(artist_router)
app.include_router(user_router)
app.include_router(song_router)
app.include_router(album_router)
app.include_router(genre_router)
app.include_router(playlist_router)
app.include_router(admin_router)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Spotify Tech API is running"
    }