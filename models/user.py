from mongoengine import Document, StringField, ListField, IntField, EmbeddedDocumentField
from models.tasks import Tasks


class User(Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    phone_number = StringField(required=False)
    password = StringField(required=True)

    tasks = ListField(EmbeddedDocumentField(Tasks))
    meta = {"collection": "Users"} #setting collection name

    def update_task(self, task_title, **kwargs):
        """updates tasks by changing key to new value"""
        task = None
        for t in self.tasks:
            if t.title == task_title:
                print(t.title)
                task = t
                break
        if not task:
            raise ValueError("Task not found")
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        self.save()
        print("Everything has been updated Successfully")
        return task

    def delete_task(self, task_title):
        task_to_delete = next(t for t in self.tasks if t.title == task_title)
        if not task_to_delete:
            raise ValueError("This task doesn't exist")
        self.tasks.remove(task_to_delete)
        self.save()
        print(f"{task_title} deleted Successfully")
        return True









