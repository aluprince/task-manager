from controllers.user_controller import register_user, login_user
from flask import request, Blueprint, jsonify
from mongoengine import get_connection


# print(get_connection(alias="default"))


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    print(data)
    result = register_user(data)
    return jsonify(result[0], result[1])


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    print(data)
    return login_user(data)

@auth_bp.route("/api/logout", methods=["GET"])
def logout():
    response = jsonify(message="Logout successful")
    response.set_cookie("access_token", ", expires=0", httponly=True, samesite="Lax")
    return response, 200
