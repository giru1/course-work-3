from project.dao.models.favorite import Favorite
from typing import Dict, Any

from marshmallow import ValidationError

from project.dao.base import BaseDAO


class FavoriteDAO(BaseDAO):
    def __init__(self, session):
        self.session = session
