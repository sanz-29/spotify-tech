from datetime import datetime

from pydantic import BaseModel


class PlaylistCreate(BaseModel):
    name: str
    description: str | None = None


class PlaylistResponse(BaseModel):
    playlist_id: int
    name: str
    description: str | None
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PlaylistSongCreate(BaseModel):
    song_id: int


class PlaylistSongResponse(BaseModel):
    playlist_id: int
    song_id: int
    added_at: datetime

    class Config:
        from_attributes = True
