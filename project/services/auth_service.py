from flask import request

from flask_restx import abort
from utils import get_hashed_pass, genereta_tokens, decode_token

from setup_db import db
from dao.user import UserDAO
from service.user import UserService

user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)


class AuthService:
    def __init__(self, user_service: user_service):
        self.user_service = user_service

    def login(self, data: dict):
        user_data = self.user_service.get_by_username(data['username'])
        if user_data is None:
            abort(401, message='user not found')

        hashed_pass = get_hashed_pass(data['password'])
        if user_data.password != hashed_pass:
            abort(401, message='No correct data')

        tokens: dict = genereta_tokens(
            {
                'username': data['username'],
                'role': user_data.role
            }
        )
        return tokens

    def get_new_token(self, refresh_token: str):
        decoded_token = decode_token(refresh_token, refresh_token=True)

        token = genereta_tokens(
            data={
                'username': decoded_token['username'],
                'role': decoded_token['role']
            }
        )
        return token