from project.dao.models.user import User
from typing import Dict, Any


from marshmallow import ValidationError

from project.dao.base import BaseDAO


class UserDAO(BaseDAO):
    def __init__(self, session):
        self.session = session

    def get_by_username(self, username):

        return self.session.query(User).filter(User.email == username).first()

    def get_one(self, bid):
        return self.session.query(User).filter(User.id == bid).first()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        # print(user_d)
        user = User(**user_d)
        self.session.add(user)
        self.session.commit()

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, data, user_id):
        self.session.query(User).filter(User.id == user_id).update(data)
        self.session.commit()
