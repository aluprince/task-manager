from flask import jsonify, Blueprint, request
from controllers.tasks_controller import create_task, read_tasks, update_task, delete_tasks
from functools import wraps
from Jwt_helpers.helper_tokens import decode_token
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

task_bp = Blueprint("task", __name__)


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        print("HEADERS:", request.headers)

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            print("Authorization header:", auth_header)

            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
            else:
                return jsonify({"error": "Authorization header must be 'Bearer <token>'"}), 401

        if not token:
            token = request.cookies.get("access_token")
            print(token)

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        decode = decode_token(token=token, token_type="access")

        if "error" in decode:
            return jsonify({decode}), 401

        request.user = decode
        # print(request.user)
        return func(*args, **kwargs)
    return decorated


@task_bp.route("/create-task", methods=["POST"])
@token_required
def create():
    current_user = request.user  # from token (user info)
    print(current_user)
    username = current_user["user_identity"]["name"] # get the current user name
    print(username)
    data = request.get_json()    # from frontend (task data)

    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")

    return create_task(
        username=username,
        title=title,
        description=description,
        due_date=due_date
    )


@task_bp.route("/read")
@token_required
def read():
    current_user = request.user
    print(current_user)
    return read_tasks(current_user["user_identity"]["name"])


@task_bp.route("/update-task", methods=["PATCH"])
@token_required
def update(**kwargs):
    current_user = request.user
    data = request.get_json()
    task_title = data.get("task_title")

    kwargs = {key: value for key, value in data.items() if key not in ["name", "task_title"]}

    return update_task(username=current_user["name"], task_title=task_title, **kwargs)


@task_bp.route("/delete", methods=["DELETE"])
@token_required
def delete():
    current_user = request.user
    data = request.json
    title = data["title"]
    return delete_tasks(username=current_user["user_identity"]["name"], task_title=title), 200
