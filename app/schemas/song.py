from pydantic import BaseModel, ConfigDict, Field


class SongCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    artist_id: int = Field(..., ge=1)
    album_id: int | None = None
    genre_id: int | None = None
    audio_url: str = Field(..., min_length=1, max_length=255)
    cover_image_url: str | None = Field(default=None, max_length=255)
    duration: int = Field(..., ge=0)


class SongResponse(BaseModel):
    song_id: int
    title: str
    artist_id: int
    album_id: int | None
    genre_id: int | None
    audio_url: str
    cover_image_url: str | None
    duration: int

    model_config = ConfigDict(from_attributes=True)