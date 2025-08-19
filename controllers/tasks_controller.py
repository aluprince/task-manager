from models.tasks import Tasks
from models.user import User
from flask import jsonify


def create_task(data):
    try:
        user = User.objects(name=data["name"]).first()

        task = Tasks(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            status=data["status"],
        )

        user.tasks.append(task)
        user.save()

        return jsonify(message="Task saved successfully"), 201

    except Exception as e:
        print(f"This is the cause: {e}")
        return jsonify(error=str(e)), 400


def read_tasks(username):
    try:
        user = User.objects(name=username).first()
        print(user)
    except Exception as e:
        print(f"This is the cause: {e}")


def update_task(username, task_title, **kwargs):
    # Later change to get user by id instead of relying on name which might be the same
    """This function takes username, task title and any **kwargs which can be either(title, description, due_date, status)"""
    try:
        user = User.objects(name=username).first()
        print(user)
        if not user:
            raise ValueError("User does not exist")
        user.update_task(task_title, **kwargs)
        user.save()
        return jsonify(message="Tasks has been updated successfully")

    except Exception as e:
        print(f"This is the cause: {e}")

