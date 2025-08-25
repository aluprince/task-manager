from models.tasks import Tasks
from models.user import User
from flask import jsonify


def create_task(username, title, description, due_date):
    try:
        user = User.objects(name=username).first()

        task = Tasks(
            title=title,
            description=description,
            due_date=due_date,
            status="pending"
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
        if not user:
            raise ValueError("This user does not exist")
        else:
            tasks_list = []
            for task in user.tasks:
                if task:
                    tasks_list.append({
                        "title": task.title,
                        "description": task.description,
                        "due_date": task.due_date,
                        "status": task.status
                    })
            if not tasks_list:
                raise ValueError("There are no tasks available")
        return jsonify({"tasks": tasks_list}), 200
    except Exception as e:
        print(f"This is the cause: {e}"), 400


def update_task_status(username, task_title):
    """ This function updates the user status for now, later it will update tasks"""

    # Later change to get user by id instead of relying on name which might be the same
    try:
        user = User.objects(name=username).first()
        print(user)
        if not user:
            raise ValueError("User does not exist")
        # user.update_task(task_title, **kwargs)
        user.update_status(task_title)
        user.save()
        return jsonify(message="Tasks has been updated successfully")

    except Exception as e:
        print(f"This is the cause: {e}"), 400


def delete_tasks(username, task_title):
    try:
        user = User.objects(name=username).first()
        user.delete_task(task_title=task_title)
    except ValueError:
        print("There was no task which such title")
    return jsonify(message="Deleted Successfully")

