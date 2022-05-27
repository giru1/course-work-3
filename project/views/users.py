from flask import request, abort
from flask_restx import Resource, Namespace

from project.schemas.user import UserSchema
from project.implemented import user_service
from project.utils import auth_required

users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200


@users_ns.route('/<int:user_id>')
class UserView(Resource):
    @auth_required
    def get(self, user_id):
        r = user_service.get_one(user_id)
        # sm_d = UserSchema().dump(r)
        return r, 200

    @auth_required
    def patch(self, user_id):
        user_data = request.json
        user_service.update(user_data, user_id)

    @auth_required
    def delete(self, user_id):
        return user_service.delete(user_id)

    @auth_required
    def put(self, user_id):
        req_json = request.json
        # if "id" not in req_json:
        #     req_json["id"] = user_id
        user_service.update(req_json)
        return "", 204


@users_ns.route("/<user_id>/password")
class PasswordResetView(Resource):
    # @auth_required
    def put(self, user_id):
        print(request.json)
        user_service.reset_password(user_id, request.json)
        return "OK", 200
