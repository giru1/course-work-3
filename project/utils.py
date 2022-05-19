import json
import base64
import hashlib
from datetime import timedelta, datetime
from typing import Dict

import jwt
from flask import request
from flask_restx import abort
from setup_db import db
from config import BaseConfig
from dao.user import UserDAO
from services.user_service import UserService

user_dao = UserDAO(session=db.session)
user_service = UserService(dao=user_dao)


def read_json(filename, encoding="utf-8"):
    """
    Считываем json
    :param filename: Название файла
    :param encoding: Кодировка для декодирования
    :return: объект Python
    """
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def get_hashed_pass(password: str) -> str:
    """
    Хешируем пароль
    :param password: Пароль в виде строки
    :return: Хешированный пароль
    """
    return base64.b64encode(hashlib.pbkdf2_hmac(
        hash_name=BaseConfig.HASH_NAME,
        salt=BaseConfig.PWD_HASH_SALT.encode('utf-8'),
        iterations=BaseConfig.PWD_HASH_ITERATIONS,
        password=password.encode('utf-8')
    )).decode('utf-8', "ignore")


def generation_tokens(data: dict) -> Dict[str, str]:
    """
    Генерируем токены
    :param data: Словарь с токенами
    :return: Словарь с токенами
    """
    data['exp'] = datetime.utcnow() + timedelta(minutes=30)
    data['refresh_token'] = False

    access_token: str = jwt.encode(
        payload=data,
        key=BaseConfig.SECRET_KEY,
        algorithm=BaseConfig.JWT_ALGORITHM,
    )

    data['exp'] = datetime.utcnow() + timedelta(days=30)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=BaseConfig.SECRET_KEY,
        algorithm=BaseConfig.JWT_ALGORITHM,
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_token_headers(headers: dict):
    """
    Получаем токен из заголовка авторизации
    :param headers:
    :return:
    """
    if 'Authorization' not in headers:
        abort(401)

    return headers['Authorization'].split(' ')[-1]


def decode_token(token: str, refresh_token: bool = False):
    """
    Декодируем токен
    :param token: access токен
    :param refresh_token: refresh токен
    :return: Возвращаем декодированный токен
    """
    decoded_token = {}
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=BaseConfig.SECRET_KEY,
            algorithms=[BaseConfig.JWT_ALGORITHM],
        )
    except jwt.PyJWTError as e:
        abort(401, message='no valid token')

    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='wrong token type')

    return decoded_token


def auth_required(func):
    """
    Декоратор проверки авторизации
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        token = get_token_headers(request.headers)
        decoded_token = decode_token(token)
        print(decoded_token['username'])
        print(decoded_token)
        print(type(decoded_token))
        if not user_service.get_by_username(decoded_token.get('username')):
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_access_required(func):
    """
    Декоратор проверки админа
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        token = get_token_headers(request.headers)

        decoded_token = decode_token(token)
        if decoded_token['role'] != 'admin':
            abort(403)
        return func(*args, **kwargs)

    return wrapper


print(get_hashed_pass('542525'))