from pydantic import BaseModel, Field


class GenreCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class GenreResponse(BaseModel):
    genre_id: int
    name: str

    class Config:
        from_attributes = True
