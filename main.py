from os import environ

from app import create_app

app = create_app(environ.get('FLASK_ENV') or 'development')

if __name__ == '__main__':
    app.run()
