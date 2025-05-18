from flask.views import MethodView


class MovieController(MethodView):
    def get(self):
        return 'MovieController GET method'

    def post(self):
        return 'MovieController POST method'

    def put(self):
        return 'MovieController PUT method'

    def delete(self):
        return 'MovieController DELETE method'
