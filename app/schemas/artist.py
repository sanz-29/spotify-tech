from pydantic import BaseModel


class ArtistCreate(BaseModel):
    name: str
    bio: str | None = None
    image_url: str | None = None