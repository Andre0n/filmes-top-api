from typing import Dict, List
from wsgiref.headers import Headers
from flask.testing import FlaskClient

CreateMovieData = Dict[str, int | str]

class TestMovieController:
    def test_create_movie_success(self, client: FlaskClient, auth_headers: Headers):
        """Test successful movie creation"""
        data:CreateMovieData = {
            "title": "The Shawshank Redemption",
            "year": 1994,
            "genre": "Drama",
            "duration": 142
        }


        response = client.post('/api/movies', json=data, headers=auth_headers)
        if response.status_code == 308:
            redirect_location = response.headers.get('Location')
            if redirect_location:
                response = client.post(redirect_location, json=data, headers=auth_headers)
    
        assert response.status_code == 201
        assert response.json is not None
        assert response.json['title'] == data['title']
        assert response.json['year'] == data['year']

    def test_create_movie_duplicate(self, client: FlaskClient, auth_headers: Headers):
        """Test creating a movie with duplicate title"""
        # First creation
        data1: CreateMovieData = {
            "title": "Duplicate Movie",
            "year": 2020,
            "genre": "Comedy",
            "duration": 90
        }
        response = client.post('/api/movies', json=data1, headers=auth_headers)
        if response.status_code == 308:
            redirect_location = response.headers.get('Location')
            if redirect_location:
                response = client.post(redirect_location, json=data1, headers=auth_headers)
        
        # Second creation with same title
        data2: CreateMovieData = {
            "title": "Duplicate Movie",
            "year": 2021,
            "genre": "Action",
            "duration": 120
        }
        response = client.post('/api/movies', json=data2, headers=auth_headers)
        if response.status_code == 308:
            redirect_location = response.headers.get('Location')
            if redirect_location:
                response = client.post(redirect_location, json=data2, headers=auth_headers)
        
        assert response.json
        assert response.status_code == 409
        assert response.json['message'] == "Um filme com esse título já existe"

    def test_get_movies(self, client: FlaskClient, auth_headers: Headers):
        """Test getting list of movies"""
        # Create some test movies
        movies: List[CreateMovieData] = [
            {"title": "Movie 1", "year": 2000, "genre": "Action", "duration": 120},
            {"title": "Movie 2", "year": 2005, "genre": "Comedy", "duration": 90},
            {"title": "Movie 3", "year": 2010, "genre": "Drama", "duration": 110}
        ]
        for movie in movies:
            response = client.post('/api/movies/', json=movie, headers=auth_headers)
            if response.status_code == 308:
                redirect_location = response.headers.get('Location')
                response = client.post(redirect_location, json=movie, headers=auth_headers)
            assert response.status_code == 201
        
        response = client.get('/api/movies/', headers=auth_headers)
        if response.status_code == 308:
            redirect_location = response.headers.get('Location')
            response = client.get(redirect_location, headers=auth_headers)
        
        assert response.json
        assert response.status_code == 200
        assert len(response.json['movies']['data']) >= 3  # At least the 3 we created

    def test_get_movie_by_id(self, client: FlaskClient, auth_headers: Headers, test_movie: Dict[str, int | str]):
        """Test getting a specific movie by ID"""
        movie_id = test_movie['id']
        response = client.get(f'/api/movies/{movie_id}', headers=auth_headers)
        if response.status_code == 308:
            redirect_location = response.headers.get('Location')
            response = client.get(redirect_location, headers=auth_headers)
        assert response.json
        assert response.status_code == 200
        assert response.json['id'] == movie_id
        assert response.json['title'] == "Inception"

    def test_get_movie_not_found(self, client: FlaskClient, auth_headers: Headers):
        """Test getting a non-existent movie"""
        response = client.get('/api/movies/nonexistent', headers=auth_headers)
        
        assert response.status_code == 404

    def test_get_movies_with_filters(self, client: FlaskClient, auth_headers: Headers):
        """Test getting movies with search and genre filters"""
        # Create test movies
        test_movies: List[CreateMovieData]  = [
            {"title": "Sci-Fi Movie", "year": 2020, "genre": "Sci-Fi", "duration": 120},
            {"title": "Action Movie", "year": 2019, "genre": "Action", "duration": 110},
            {"title": "Another Sci-Fi", "year": 2018, "genre": "Sci-Fi", "duration": 95}
        ]
        for movie in test_movies:
            response = client.post('/api/movies/', json=movie, headers=auth_headers)
            if response.status_code == 308:
                redirect_location = response.headers.get('Location')
                response = client.post(redirect_location, json=movie, headers=auth_headers)
            assert response.status_code == 201
        
        # Test search filter
        search_response = client.get(
            '/api/movies?search=Sci-Fi', 
            headers=auth_headers
        )

        if search_response.status_code == 308:
            search_redirect_location = search_response.headers.get('Location')
            search_response = client.get(search_redirect_location, headers=auth_headers)

        assert search_response.json
        assert search_response.status_code == 200
        assert len(search_response.json['movies']['data']) == 2
        
        # Test genre filter
        genre_response = client.get(
            '/api/movies?genre=Action', 
            headers=auth_headers
        )

        if genre_response.status_code == 308:
            genre_redirect_location = genre_response.headers.get('Location')
            genre_response = client.get(genre_redirect_location, headers=auth_headers)

        assert genre_response.json
        assert genre_response.status_code == 200
        assert len(genre_response.json['movies']) == 1
