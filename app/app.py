from fastapi import FastAPI

from app.database import Base, engine
from app.models import user, artist

from app.api.artist import router as artist_router
from app.api.user import router as user_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Spotify Tech API",
    version="1.0.0"
)


app.include_router(artist_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "Spotify Tech API is running"
    }
