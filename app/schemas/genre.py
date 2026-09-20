from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str


class GenreResponse(BaseModel):
    genre_id: int
    name: str

    class Config:
        from_attributes = True
