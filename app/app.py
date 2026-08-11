from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, artist
from app.api.artist import router as artist_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Spotify Tech API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Spotify Tech API is running"
    }


app.include_router(artist_router)