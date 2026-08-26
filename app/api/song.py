from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.song import Song
from app.schemas.song import SongCreate, SongResponse

router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)


@router.post("/", response_model=SongResponse)
def create_song(
    song: SongCreate,
    db: Session = Depends(get_db)
):
    new_song = Song(
        title=song.title,
        artist_id=song.artist_id,
        album_id=song.album_id,
        genre_id=song.genre_id,
        audio_url=song.audio_url,
        cover_image_url=song.cover_image_url,
        duration=song.duration
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return new_song


@router.get("/", response_model=list[SongResponse])
def get_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()


@router.get("/{song_id}", response_model=SongResponse)
def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Song).filter(
        Song.song_id == song_id
    ).first()