from controllers.user_controller import register_user, login_user
from flask import request, Blueprint


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    print(data)
    return register_user(data)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    print(data)
    return login_user(data)