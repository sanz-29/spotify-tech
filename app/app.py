from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import user, artist, song

from app.api.artist import router as artist_router
from app.api.user import router as user_router
from app.api.song import router as song_router


# Create FastAPI application
app = FastAPI(
    title="Spotify Tech API",
    version="1.0.0"
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


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Spotify Tech API is running"
    }