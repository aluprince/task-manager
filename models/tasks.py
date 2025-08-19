from mongoengine import EmbeddedDocument, StringField, ListField, DictField


class Tasks(EmbeddedDocument):
    title = StringField(required=True, max_length=100)
    description = StringField()
    due_date = StringField()
    status = StringField()

    meta = {"collections": "Tasks"}

