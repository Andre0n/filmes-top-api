from typing import Optional

from pydantic import BaseModel, Field


class GetMovieRequest(BaseModel):
    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=100, ge=1, le=100)
    search: Optional[str] = Field(default=None, max_length=100)
