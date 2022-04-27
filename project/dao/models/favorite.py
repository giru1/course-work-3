from project.dao.models.base import BaseMixin
from project.setup_db import db


class Favorite(BaseMixin, db.Model):
    __tablename__ = "favorite"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)
    movie = db.relationship("Movie")