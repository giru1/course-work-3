from flask import request
from flask_restx import Resource, Namespace
# from project.dao.models.user import UserSchema
from project.implemented import user_service
auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        print(request.json)
        user_service.create(request.json)
        return {}, 201


@auth_ns.route('/login')
class AuthLoginView(Resource):
    def post(self):
        pass

    def put(self):
        pass
