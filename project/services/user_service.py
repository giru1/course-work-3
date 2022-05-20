from project.dao.user import UserDAO
from project.services.base import BaseService


class UserService(BaseService):
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_by_username(self, username):
        # print(data)
        return self.dao.get_by_username(username)

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d: dict):
        return self.dao.create(user_d)

    def update(self, user_d: dict):
        self.dao.update(user_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
