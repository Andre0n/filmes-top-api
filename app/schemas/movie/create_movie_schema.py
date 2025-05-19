from pydantic import BaseModel, Field


class CreateMovieRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., gt=1888, lt=2100)
    genre: str = Field(..., min_length=1, max_length=50)
    duration: int = Field(..., gt=0)
