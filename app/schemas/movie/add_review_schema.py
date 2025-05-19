from typing import Optional

from pydantic import BaseModel, Field


class AddReviewRequest(BaseModel):
    rating: float = Field(..., ge=0, le=10)
    comment: Optional[str] = Field(None, max_length=500)
