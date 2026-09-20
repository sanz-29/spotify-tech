from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_artist
from app.models.album import Album
from app.models.artist import Artist
from app.models.user import User
from app.schemas.album import AlbumCreate, AlbumResponse


router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
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


def get_owned_album(
    album_id: int,
    current_user: User,
    db: Session
) -> Album:
    album = db.query(Album).filter(
        Album.album_id == album_id
    ).first()

    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    if current_user.role != "admin":
        if album.artist_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Album is not associated with an artist"
            )
        get_artist_for_user(album.artist_id, current_user, db)

    return album


@router.post(
    "/",
    response_model=AlbumResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_album(
    album: AlbumCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    artist_id = album.artist_id
    if current_user.role != "admin":
        if current_user.artist is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artist profile not found"
            )
        if artist_id is None:
            artist_id = current_user.artist.artist_id
        get_artist_for_user(artist_id, current_user, db)
    elif artist_id is not None:
        get_artist_for_user(artist_id, current_user, db)

    new_album = Album(
        title=album.title,
        artist_id=artist_id,
        release_date=album.release_date,
        cover_image_url=album.cover_image_url
    )

    db.add(new_album)
    db.commit()
    db.refresh(new_album)

    return new_album


@router.get("/", response_model=list[AlbumResponse], summary="List albums")
def get_albums(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Album).offset((page - 1) * limit).limit(limit).all()


@router.get("/search", response_model=list[AlbumResponse], summary="Search albums")
def search_albums(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db)
):
    return db.query(Album).filter(Album.title.ilike(f"%{q}%")).limit(100).all()


@router.get("/{album_id}", response_model=AlbumResponse)
def get_album(
    album_id: int,
    db: Session = Depends(get_db)
):
    album = db.query(Album).filter(
        Album.album_id == album_id
    ).first()

    if album is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    return album


@router.put("/{album_id}", response_model=AlbumResponse)
def update_album(
    album_id: int,
    album_data: AlbumCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    album = get_owned_album(album_id, current_user, db)

    if current_user.role != "admin":
        if album_data.artist_id is not None and album_data.artist_id != album.artist_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot change album ownership"
            )
        artist_id = album.artist_id
    else:
        artist_id = album_data.artist_id
        if artist_id is not None:
            get_artist_for_user(artist_id, current_user, db)

    album.title = album_data.title
    album.artist_id = artist_id
    album.release_date = album_data.release_date
    album.cover_image_url = album_data.cover_image_url

    db.commit()
    db.refresh(album)

    return album


@router.delete("/{album_id}")
def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    album = get_owned_album(album_id, current_user, db)
    db.delete(album)
    db.commit()

    return {
        "message": "Album deleted successfully"
    }
