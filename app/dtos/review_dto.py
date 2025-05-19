from dataclasses import dataclass, field
from typing import List, Optional

from ..models import Review


@dataclass
class ReviewDto:
    id: Optional[int] = field(default=None)
    created_at: Optional[str] = field(default=None)
    rating: float = field(default=0)
    comment: Optional[str] = field(default=None)
    user_name: Optional[str] = field(default=None)

    @classmethod
    def from_model(cls, review: Review) -> 'ReviewDto':
        return cls(
            id=review.id,
            created_at=review.created_at.isoformat(),
            rating=review.rating,
            comment=review.comment,
            user_name=review.user.name,
        )


@dataclass
class ListReviewResponseDto:
    data: List[ReviewDto] = field(default_factory=List[ReviewDto])

    @classmethod
    def from_model(cls, reviews: list[Review]) -> 'ListReviewResponseDto':
        return cls(data=[ReviewDto.from_model(review) for review in reviews])
