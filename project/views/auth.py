from flask import request
from flask_restx import Resource, Namespace

auth_ns = Namespace('auth')


@auth_ns.route('/auth/register')
class AuthRegisterView(Resource):
    def post(self):
        print(request.json)


@auth_ns.route('/auth/login')
class AuthLoginView(Resource):
    def post(self):
        pass

    def put(self):
        pass
