from ..extensions import db
from ..models import Review


class ReviewRepository:
    def __init__(self):
        self.session = db.session

    def create(
        self, user_id: str, movie_id: str, rating: float, comment: str | None
    ) -> Review:
        review = Review(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
            comment=comment,
        )
        self.session.add(review)
        self.session.commit()
        return review

    def find_by_user_and_movie(
        self, user_id: str, movie_id: str
    ) -> Review | None:
        return (
            self.session.query(Review)
            .filter_by(user_id=user_id, movie_id=movie_id)
            .first()
        )
