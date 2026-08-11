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