from datetime import date

from pydantic import BaseModel, Field


class AlbumCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    artist_id: int | None = None
    release_date: date | None = None
    cover_image_url: str | None = Field(default=None, max_length=255)


class AlbumResponse(BaseModel):
    album_id: int
    title: str
    artist_id: int | None
    release_date: date | None
    cover_image_url: str | None

    class Config:
        from_attributes = True
