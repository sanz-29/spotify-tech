from pydantic import BaseModel, ConfigDict, Field


class GenreCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class GenreResponse(BaseModel):
    genre_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
