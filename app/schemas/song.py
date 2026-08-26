from pydantic import BaseModel


class SongCreate(BaseModel):
    title: str
    artist_id: int
    album_id: int | None = None
    genre_id: int | None = None
    audio_url: str
    cover_image_url: str | None = None
    duration: int


class SongResponse(BaseModel):
    song_id: int
    title: str
    artist_id: int
    album_id: int | None
    genre_id: int | None
    audio_url: str
    cover_image_url: str | None
    duration: int

    class Config:
        from_attributes = True