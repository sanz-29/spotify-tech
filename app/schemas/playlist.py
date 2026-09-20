from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlaylistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class PlaylistResponse(BaseModel):
    playlist_id: int
    name: str
    description: str | None
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlaylistSongCreate(BaseModel):
    song_id: int = Field(..., ge=1)


class PlaylistSongResponse(BaseModel):
    playlist_id: int
    song_id: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)
