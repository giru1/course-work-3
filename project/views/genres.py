from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services.genres_service import GenreService
from project.setup_db import db

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.response(200, "OK")
    def get(self):
        """Get all genres"""
        return GenreService(db.session).get_all()


@genres_ns.route("/<int:genre_id>")
class GenreView(Resource):
    @genres_ns.response(200, "OK")
    @genres_ns.response(404, "Genre not found")
    def get(self, genre_id: int):
        """Get genre by id"""
        try:
            return GenreService(db.session).get_one(genre_id)
        except ItemNotFound:
            abort(404, message="Genre not found")
