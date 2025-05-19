from flask.testing import FlaskClient


class TestAuthController:
    def test_register_success(self, client: FlaskClient):
        """Test successful user registration"""
        data = {
            "username": "newuser",
            "name": "New User",
            "email": "new@example.com",
            "password": "NewPass123"
        }
        response = client.post('/api/register', json=data)
        
        assert response.json
        assert response.status_code == 201
        assert response.json['message'] == "Usuário criado com sucesso"
        assert response.json['username'] == "newuser"
        assert response.json['name'] == "New User"
        assert response.json['email'] == "new@example.com"
        

    def test_register_duplicate(self, client: FlaskClient):
        """Test registration with duplicate email"""
        # First registration
        data1 = {
            "username": "user1",
            "name": "User One",
            "email": "duplicate@example.com",
            "password": "Pass1234"
        }
        client.post('/api/register', json=data1)
        
        # Second registration with same email
        data2 = {
            "username": "user2",
            "name": "User Two",
            "email": "duplicate@example.com",
            "password": "Pass1234"
        }
        response = client.post('/api/register', json=data2)
        
        assert response.json 
        assert response.status_code == 409
        assert response.json['message'] == "Um usuário com esse e-mail já existe"


    def test_login_success(self, client: FlaskClient):
        """Test successful login"""
        # Register first
        register_data = {
            "username": "loginuser",
            "name": "Login User",
            "email": "login@example.com",
            "password": "LoginPass123"
        }
        client.post('/api/register', json=register_data)
        
        # Then login
        login_data = {
            "email": "login@example.com",
            "password": "LoginPass123"
        }
        response = client.post('/api/login', json=login_data)
        
        assert response.json
        assert response.status_code == 200
        assert 'access_token' in response.json

    def test_login_invalid_credentials(self, client: FlaskClient):
        """Test login with invalid credentials"""
        data = {
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        }
        response = client.post('/api/login', json=data)
        
        assert response.json

        print(response.json)
        assert response.status_code == 404
        assert response.json['message'] == "Usuário não encontrado"
