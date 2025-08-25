from mongoengine import EmbeddedDocument, StringField


class Tasks(EmbeddedDocument):
    title = StringField(required=True, max_length=100)
    description = StringField()
    due_date = StringField()
    status = StringField(default="pending")

    meta = {"collections": "Tasks"}
