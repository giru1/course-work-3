from flask import request
from flask_restx import Resource, Namespace
from project.implemented import auth_service
auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        return auth_service.register(request.json)


@auth_ns.route('/login')
class AuthLoginView(Resource):
    def post(self):
        return auth_service.login(request.json)

    def put(self):
        return auth_service.login(request.json)
