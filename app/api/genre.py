from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.genre import Genre
from app.models.user import User
from app.schemas.genre import GenreCreate, GenreResponse


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


@router.post("/", response_model=GenreResponse)
def create_genre(
    genre: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    existing_genre = db.query(Genre).filter(
        Genre.name == genre.name
    ).first()

    if existing_genre is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists"
        )

    new_genre = Genre(name=genre.name)
    db.add(new_genre)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists"
        )

    db.refresh(new_genre)
    return new_genre


@router.get("/", response_model=list[GenreResponse], summary="List genres")
def get_genres(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return db.query(Genre).offset((page - 1) * limit).limit(limit).all()


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):
    genre = db.query(Genre).filter(
        Genre.genre_id == genre_id
    ).first()

    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )

    return genre


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: int,
    genre_data: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    genre = db.query(Genre).filter(
        Genre.genre_id == genre_id
    ).first()

    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )

    duplicate_genre = db.query(Genre).filter(
        Genre.name == genre_data.name,
        Genre.genre_id != genre_id
    ).first()

    if duplicate_genre is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists"
        )

    genre.name = genre_data.name
    db.commit()
    db.refresh(genre)

    return genre


@router.delete("/{genre_id}")
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    genre = db.query(Genre).filter(
        Genre.genre_id == genre_id
    ).first()

    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )

    db.delete(genre)
    db.commit()

    return {
        "message": "Genre deleted successfully"
    }
