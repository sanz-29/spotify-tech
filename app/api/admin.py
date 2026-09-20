from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.album import Album
from app.models.artist import Artist
from app.models.genre import Genre
from app.models.song import Song
from app.models.user import User
from app.schemas.album import AlbumCreate, AlbumResponse
from app.schemas.artist import ArtistCreate, ArtistResponse
from app.schemas.genre import GenreCreate, GenreResponse
from app.schemas.song import SongCreate, SongResponse
from app.schemas.user import AdminUserUpdate, UserResponse


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_user_or_404(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def get_artist_or_404(artist_id: int, db: Session) -> Artist:
    artist = db.query(Artist).filter(
        Artist.artist_id == artist_id
    ).first()
    if artist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    return artist


def get_album_or_404(album_id: int, db: Session) -> Album:
    album = db.query(Album).filter(
        Album.album_id == album_id
    ).first()
    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )
    return album


def get_song_or_404(song_id: int, db: Session) -> Song:
    song = db.query(Song).filter(
        Song.song_id == song_id
    ).first()
    if song is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    return song


def get_genre_or_404(genre_id: int, db: Session) -> Genre:
    genre = db.query(Genre).filter(
        Genre.genre_id == genre_id
    ).first()
    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return genre


def ensure_admin_remains(
    target: User,
    new_role: str | None,
    db: Session
) -> None:
    if target.role != "admin":
        return

    removing_admin = new_role is not None and new_role != "admin"
    if not removing_admin:
        return

    admin_count = db.query(User).filter(User.role == "admin").count()
    if admin_count <= 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot remove the final administrator"
        )


@router.get("/users", response_model=list[UserResponse])
def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(User).offset((page - 1) * limit).limit(limit).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_user_or_404(user_id, db)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = get_user_or_404(user_id, db)
    ensure_admin_remains(user, user_data.role, db)
    user.username = user_data.username
    user.email = user_data.email
    user.role = user_data.role

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = get_user_or_404(user_id, db)
    ensure_admin_remains(user, None, db)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.get("/artists", response_model=list[ArtistResponse])
def get_artists(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Artist).offset((page - 1) * limit).limit(limit).all()


@router.get("/artists/{artist_id}", response_model=ArtistResponse)
def get_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_artist_or_404(artist_id, db)


@router.put("/artists/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    artist_data: ArtistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    artist = get_artist_or_404(artist_id, db)
    artist.name = artist_data.name
    artist.bio = artist_data.bio
    artist.image_url = artist_data.image_url
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Artist name already exists"
        )
    db.refresh(artist)
    return artist


@router.delete("/artists/{artist_id}")
def delete_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    artist = get_artist_or_404(artist_id, db)
    db.delete(artist)
    db.commit()
    return {"message": "Artist deleted successfully"}


@router.get("/songs", response_model=list[SongResponse])
def get_songs(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Song).offset((page - 1) * limit).limit(limit).all()


@router.get("/songs/{song_id}", response_model=SongResponse)
def get_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_song_or_404(song_id, db)


def validate_song_data(song_data: SongCreate, db: Session) -> None:
    get_artist_or_404(song_data.artist_id, db)
    if song_data.album_id is not None:
        album = get_album_or_404(song_data.album_id, db)
        if album.artist_id != song_data.artist_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Album does not belong to this artist"
            )
    if song_data.genre_id is not None:
        get_genre_or_404(song_data.genre_id, db)


@router.put("/songs/{song_id}", response_model=SongResponse)
def update_song(
    song_id: int,
    song_data: SongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    song = get_song_or_404(song_id, db)
    validate_song_data(song_data, db)
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


@router.delete("/songs/{song_id}")
def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    song = get_song_or_404(song_id, db)
    db.delete(song)
    db.commit()
    return {"message": "Song deleted successfully"}


@router.get("/albums", response_model=list[AlbumResponse])
def get_albums(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Album).offset((page - 1) * limit).limit(limit).all()


@router.get("/albums/{album_id}", response_model=AlbumResponse)
def get_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_album_or_404(album_id, db)


@router.put("/albums/{album_id}", response_model=AlbumResponse)
def update_album(
    album_id: int,
    album_data: AlbumCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    album = get_album_or_404(album_id, db)
    if album_data.artist_id is not None:
        get_artist_or_404(album_data.artist_id, db)
    album.title = album_data.title
    album.artist_id = album_data.artist_id
    album.release_date = album_data.release_date
    album.cover_image_url = album_data.cover_image_url
    db.commit()
    db.refresh(album)
    return album


@router.delete("/albums/{album_id}")
def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    album = get_album_or_404(album_id, db)
    db.delete(album)
    db.commit()
    return {"message": "Album deleted successfully"}


@router.get("/genres", response_model=list[GenreResponse])
def get_genres(
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Genre).offset((page - 1) * limit).limit(limit).all()


@router.post(
    "/genres",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_genre(
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if db.query(Genre).filter(Genre.name == genre_data.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists"
        )
    genre = Genre(name=genre_data.name)
    db.add(genre)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists"
        )
    db.refresh(genre)
    return genre


@router.get("/genres/{genre_id}", response_model=GenreResponse)
def get_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return get_genre_or_404(genre_id, db)


@router.put("/genres/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: int,
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    genre = get_genre_or_404(genre_id, db)
    duplicate = db.query(Genre).filter(
        Genre.name == genre_data.name,
        Genre.genre_id != genre_id
    ).first()
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists"
        )
    genre.name = genre_data.name
    db.commit()
    db.refresh(genre)
    return genre


@router.delete("/genres/{genre_id}")
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    genre = get_genre_or_404(genre_id, db)
    db.delete(genre)
    db.commit()
    return {"message": "Genre deleted successfully"}
