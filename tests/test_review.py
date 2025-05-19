from typing import Dict
from wsgiref.headers import Headers

from flask.testing import FlaskClient


class TestMovieReviewController:
    def test_add_review_success(self, client: FlaskClient, auth_headers: Headers, test_movie: Dict[str, int | str]):
        """Test successfully adding a review to a movie"""
        # First rent the movie
        movie_id = test_movie['id']
        client.post(f'/api/movies/{movie_id}/rent', headers=auth_headers)
        
        # Then add review
        review_data: Dict[str, int| str] = {
            "rating": 5,
            "comment": "Excellent movie!"
        }
        response = client.post(
            f'/api/movies/{movie_id}/rate', 
            json=review_data, 
            headers=auth_headers
        )
        print(response.json)

        assert response.json
        assert response.status_code == 200
        assert response.json['rating'] == 5.0

    def test_add_review_not_rented(self, client: FlaskClient, auth_headers: Headers, test_movie: Dict[str, int | str]):
        """Test adding a review to a movie not rented by the user"""
        movie_id = test_movie['id']
        review_data: Dict[str, int| str] = {
            "rating": 4,
            "comment": "Good movie"
        }
        response = client.post(
            f'/api/movies/{movie_id}/rate', 
            json=review_data, 
            headers=auth_headers
        )
        
        assert response.json
        assert response.status_code == 400
        assert response.json['message'] == "Tentativa de avaliar um filme que não foi alugado"

    def test_add_review_already_reviewed(self, client: FlaskClient, auth_headers: Headers, test_movie: Dict[str, int | str]):
        """Test adding a review to a movie already reviewed by the user"""
        movie_id = test_movie['id']
        # Rent and review first time
        client.post(f'/api/movies/{movie_id}/rent', headers=auth_headers)
        review_data1: Dict[str, int| str] = {
            "rating": 5,
            "comment": "First review"
        }
        client.post(
            f'/api/movies/{movie_id}/rate', 
            json=review_data1, 
            headers=auth_headers
        )
        
        # Second review attempt
        review_data2: Dict[str, int| str] = {
            "rating": 4,
            "comment": "Second review"
        }
        response = client.post(
            f'/api/movies/{movie_id}/rate', 
            json=review_data2, 
            headers=auth_headers
        )
        assert response.json
        assert response.status_code == 409
        assert response.json['message'] == "Tentativa de avaliar um filme que já foi avaliado"
