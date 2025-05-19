from typing import Dict
from wsgiref.headers import Headers
from flask.testing import FlaskClient


class TestMovieRentalController:
    def test_rent_movie_success(self, client: FlaskClient, auth_headers: Headers, test_movie: Dict[str, int | str]):
        """Test successfully renting a movie"""
        movie_id = test_movie['id']
        response = client.post(f'/api/movies/{movie_id}/rent', headers=auth_headers)

        assert response.json
        assert response.status_code == 200
        assert response.json['message'] == "Filme alugado com sucesso"


        rental_response = client.get(
            '/api/movies?rented=true', 
            headers=auth_headers
        )

        if rental_response.status_code == 308:
            redirect_location = rental_response.headers.get('Location')
            rental_response = client.get(
                redirect_location, 
                headers=auth_headers
            )
        assert rental_response.json
        assert len(rental_response.json['movies']['data']) == 1
        assert rental_response.json['movies']['data'][0]['id'] == movie_id

    def test_rent_movie_already_rented(self, client: FlaskClient, auth_headers: Headers, test_movie: Dict[str, int | str]):
        """Test renting a movie that's already rented by the user"""
        movie_id = test_movie['id']
        # First rental
        client.post(f'/api/movies/{movie_id}/rent', headers=auth_headers)
        
        # Second rental attempt
        response = client.post(
            f'/api/movies/{movie_id}/rent', 
            headers=auth_headers
        )
        assert response.json
        assert response.status_code == 409
        assert response.json['message'] == "O filme já está alugado"

    def test_rent_movie_not_found(self, client: FlaskClient, auth_headers: Headers):
        """Test renting a non-existent movie"""
        response = client.post(
            '/api/movies/nonexistent/rent', 
            headers=auth_headers
        )
        
        assert response.status_code == 404
