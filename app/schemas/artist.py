from pydantic import BaseModel, ConfigDict, Field


class ArtistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: str | None = Field(default=None, max_length=5000)
    image_url: str | None = Field(default=None, max_length=255)


class ArtistResponse(BaseModel):
    artist_id: int
    name: str
    bio: str | None
    image_url: str | None

    model_config = ConfigDict(from_attributes=True)