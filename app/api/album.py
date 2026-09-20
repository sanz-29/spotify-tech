from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.album import Album
from app.models.artist import Artist
from app.schemas.album import AlbumCreate, AlbumResponse


router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)


@router.post("/", response_model=AlbumResponse)
def create_album(
    album: AlbumCreate,
    db: Session = Depends(get_db)
):
    if album.artist_id is not None:
        artist = db.query(Artist).filter(
            Artist.artist_id == album.artist_id
        ).first()

        if artist is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artist not found"
            )

    new_album = Album(
        title=album.title,
        artist_id=album.artist_id,
        release_date=album.release_date,
        cover_image_url=album.cover_image_url
    )

    db.add(new_album)
    db.commit()
    db.refresh(new_album)

    return new_album


@router.get("/", response_model=list[AlbumResponse])
def get_albums(db: Session = Depends(get_db)):
    return db.query(Album).all()


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

    if album_data.artist_id is not None:
        artist = db.query(Artist).filter(
            Artist.artist_id == album_data.artist_id
        ).first()

        if artist is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artist not found"
            )

    album.title = album_data.title
    album.artist_id = album_data.artist_id
    album.release_date = album_data.release_date
    album.cover_image_url = album_data.cover_image_url

    db.commit()
    db.refresh(album)

    return album


@router.delete("/{album_id}")
def delete_album(
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

    db.delete(album)
    db.commit()

    return {
        "message": "Album deleted successfully"
    }
