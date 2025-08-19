from flask import jsonify, Blueprint, request
from controllers.tasks_controller import create_task, read_tasks, update_task

task_bp = Blueprint("task", __name__)

@task_bp.route("/create-task", methods=["POST"])
def create():
    data = request.json
    print(data)
    return create_task(data)

@task_bp.route("/read")
def read():
    name = request.json["name"]
    return read_tasks(name)


@task_bp.route("/update-task", methods=["POST"])
def update(**kwargs):
    data = request.get_json()
    name = data.get("name")
    task_title = data.get("task_title")

    kwargs = {key: value for key, value in data.items() if key not in ["name", "task_title"]}

    return update_task(username=name, task_title=task_title, **kwargs)
