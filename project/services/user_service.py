from flask import request, abort
import base64
import hashlib

from project.config import BaseConfig as config
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

    def update(self, user_id, data):
        return self.dao.update(user_id, data)

    def delete(self, rid):
        self.dao.delete(rid)

    def reset_password(self, data):
        if 'Authorization' not in data.headers:
            abort(401)

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if old_password != new_password:
            self.dao.update(get_hashed_pass(new_password))


def get_hashed_pass(password: str) -> str:
    """
    Хешируем пароль
    :param password: Пароль в виде строки
    :return: Хешированный пароль
    """
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name=config.HASH_NAME,
        salt=config.PWD_HASH_SALT.encode('utf-8'),
        iterations=config.PWD_HASH_ITERATIONS,
        password=password.encode('utf-8')
    )).decode('utf-8', "ignore")