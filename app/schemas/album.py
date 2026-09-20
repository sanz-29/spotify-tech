from datetime import date

from pydantic import BaseModel


class AlbumCreate(BaseModel):
    title: str
    artist_id: int | None = None
    release_date: date | None = None
    cover_image_url: str | None = None


class AlbumResponse(BaseModel):
    album_id: int
    title: str
    artist_id: int | None
    release_date: date | None
    cover_image_url: str | None

    class Config:
        from_attributes = True
