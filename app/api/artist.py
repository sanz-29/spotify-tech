from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_artist
from app.models.artist import Artist
from app.models.user import User
from app.schemas.artist import ArtistCreate, ArtistResponse


router = APIRouter(
    prefix="/artists",
    tags=["Artists"]
)


def get_managed_artist(
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


@router.post(
    "/",
    response_model=ArtistResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_artist(
    artist: ArtistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    if current_user.role == "artist":
        existing_artist = db.query(Artist).filter(
            Artist.user_id == current_user.user_id
        ).first()

        if existing_artist is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Artist profile already exists"
            )

        user_id = current_user.user_id
    else:
        user_id = None

    new_artist = Artist(
        user_id=user_id,
        name=artist.name,
        bio=artist.bio,
        image_url=artist.image_url
    )

    db.add(new_artist)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Artist name already exists"
        )

    db.refresh(new_artist)
    return new_artist


@router.get("/", response_model=list[ArtistResponse], summary="List artists")
def get_artists(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Artist).offset((page - 1) * limit).limit(limit).all()


@router.get("/search", response_model=list[ArtistResponse], summary="Search artists")
def search_artists(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db)
):
    return db.query(Artist).filter(Artist.name.ilike(f"%{q}%")).limit(100).all()


@router.get("/me", response_model=ArtistResponse, summary="Get the current artist profile")
def get_my_artist_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_artist)
):
    artist = db.query(Artist).filter(
        Artist.user_id == current_user.user_id
    ).first()
    if artist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist profile not found"
        )
    return artist


@router.get("/{artist_id}", response_model=ArtistResponse)
def get_artist(
    artist_id: int,
    db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(
        Artist.artist_id == artist_id
    ).first()

    if artist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )

    return artist


@router.put("/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int,
    artist_data: ArtistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    artist = get_managed_artist(artist_id, current_user, db)
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


@router.delete("/{artist_id}")
def delete_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    artist = get_managed_artist(artist_id, current_user, db)
    db.delete(artist)
    db.commit()

    return {
        "message": "Artist deleted successfully"
    }
