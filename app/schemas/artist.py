from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    bio: str | None = None
    image_url: str | None = None


class ArtistResponse(BaseModel):
    artist_id: int
    name: str
    bio: str | None
    image_url: str | None

    class Config:
        from_attributes = True