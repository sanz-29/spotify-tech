from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_artist
from app.models.album import Album
from app.models.artist import Artist
from app.models.genre import Genre
from app.models.song import Song
from app.models.user import User
from app.schemas.song import SongCreate, SongResponse


router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)


def get_artist_for_user(
    artist_id: int,
    current_user: User,
    db: Session
) -> Artist:
    artist = db.query(Artist).filter(
        Artist.artist_id == artist_id
    ).first()

    if artist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )

    if current_user.role != "admin" and artist.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this artist"
        )

    return artist


def validate_song_relationships(
    song_data: SongCreate,
    current_user: User,
    db: Session
) -> None:
    get_artist_for_user(song_data.artist_id, current_user, db)

    if song_data.album_id is not None:
        album = db.query(Album).filter(
            Album.album_id == song_data.album_id
        ).first()
        if album is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album not found"
            )
        if album.artist_id != song_data.artist_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Album does not belong to this artist"
            )

    if song_data.genre_id is not None:
        genre = db.query(Genre).filter(
            Genre.genre_id == song_data.genre_id
        ).first()
        if genre is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )


def get_owned_song(
    song_id: int,
    current_user: User,
    db: Session
) -> Song:
    song = db.query(Song).filter(
        Song.song_id == song_id
    ).first()

    if song is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )

    get_artist_for_user(song.artist_id, current_user, db)
    return song


@router.post("/", response_model=SongResponse)
def create_song(
    song: SongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    validate_song_relationships(song, current_user, db)

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


@router.get("/", response_model=list[SongResponse], summary="List and filter songs")
def get_songs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    artist_id: int | None = Query(None, ge=1),
    album_id: int | None = Query(None, ge=1),
    genre_id: int | None = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(Song)
    if artist_id is not None:
        query = query.filter(Song.artist_id == artist_id)
    if album_id is not None:
        query = query.filter(Song.album_id == album_id)
    if genre_id is not None:
        query = query.filter(Song.genre_id == genre_id)
    return query.offset((page - 1) * limit).limit(limit).all()


@router.get("/search", response_model=list[SongResponse], summary="Search songs")
def search_songs(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db)
):
    pattern = f"%{q}%"
    return db.query(Song).outerjoin(Artist).outerjoin(Album).outerjoin(
        Genre
    ).filter(
        (Song.title.ilike(pattern)) |
        (Artist.name.ilike(pattern)) |
        (Album.title.ilike(pattern)) |
        (Genre.name.ilike(pattern))
    ).limit(100).all()


@router.get("/{song_id}", response_model=SongResponse)
def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):
    song = db.query(Song).filter(
        Song.song_id == song_id
    ).first()

    if song is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )

    return song


@router.put("/{song_id}", response_model=SongResponse)
def update_song(
    song_id: int,
    song_data: SongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    song = get_owned_song(song_id, current_user, db)
    validate_song_relationships(song_data, current_user, db)

    song.title = song_data.title
    song.artist_id = song_data.artist_id
    song.album_id = song_data.album_id
    song.genre_id = song_data.genre_id
    song.audio_url = song_data.audio_url
    song.cover_image_url = song_data.cover_image_url
    song.duration = song_data.duration

    db.commit()
    db.refresh(song)

    return song


@router.delete("/{song_id}")
def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    song = get_owned_song(song_id, current_user, db)
    db.delete(song)
    db.commit()

    return {
        "message": "Song deleted successfully"
    }
