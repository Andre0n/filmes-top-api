from flask.views import MethodView


class MovieController(MethodView):
    def get(self, movie_id: str|None = None):
        if movie_id:
            return f'MovieController GET method with movie_id: {movie_id}'
        return 'MovieController GET method'

    def post(self):
        return 'MovieController POST method'

    def put(self):
        return 'MovieController PUT method'

    def delete(self):
        return 'MovieController DELETE method'
