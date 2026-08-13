from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate


router = APIRouter(
    prefix="/artists",
    tags=["Artists"]
)


@router.post("/")
def create_artist(
    artist: ArtistCreate,
    db: Session = Depends(get_db)
):
    new_artist = Artist(
        name=artist.name,
        bio=artist.bio,
        image_url=artist.image_url
    )

    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)

    return new_artist

@router.get("/{artist_id}")
def get_artist(
    artist_id: int,
    db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(
        Artist.artist_id == artist_id
    ).first()

    if artist is None:
        return {
            "message": "Artist not found"
        }

    return artist

@router.put("/{artist_id}")
def update_artist(
    artist_id: int,
    artist_data: ArtistCreate,
    db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(
        Artist.artist_id == artist_id
    ).first()

    if artist is None:
        return {
            "message": "Artist not found"
        }

    artist.name = artist_data.name
    artist.bio = artist_data.bio
    artist.image_url = artist_data.image_url

    db.commit()
    db.refresh(artist)

    return artist

@router.delete("/{artist_id}")
def delete_artist(
    artist_id: int,
    db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(
        Artist.artist_id == artist_id
    ).first()

    if artist is None:
        return {
            "message": "Artist not found"
        }

    db.delete(artist)
    db.commit()

    return {
        "message": "Artist deleted successfully"
    }