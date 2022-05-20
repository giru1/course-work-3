from flask import request

from flask_restx import abort
from project.utils import get_hashed_pass, generation_tokens, decode_token

from project.setup_db import db
from project.dao.user import UserDAO
from project.services.user_service import UserService

user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)


class AuthService:
    def __init__(self, user_service: user_service):
        self.user_service = user_service

    def register(self, data: dict):
        """
        Регистрация пользователя
        :param data: Получаем емайл и пароль
        :return: объект user_dao
        """
        if data is None:
            abort(401, message='user data not found')

        user_data = {
                'email': data['email'],
                'password': get_hashed_pass(data['password'])
            }

        return user_dao.create(user_data)

    def login(self, data: dict):

        user_data = self.user_service.get_by_username(data['username'])
        
        if user_data is None:
            abort(401, message='user not found')

        hashed_pass = get_hashed_pass(data['password'])
        if user_data.password != hashed_pass:
            abort(401, message='No correct data')

        tokens: dict = generation_tokens(
            {
                'username': data['username'],
                'role': user_data.role
            }
        )
        return tokens

    # def get_new_token(self, refresh_token: str):
    #     decoded_token = decode_token(refresh_token, refresh_token=True)
    #
    #     token = generation_tokens(
    #         data={
    #             'username': decoded_token['username'],
    #             'role': decoded_token['role']
    #         }
    #     )
    #     return token
