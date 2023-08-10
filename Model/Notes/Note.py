from datetime import datetime


class Note:
    def __init__(self, id, title, body, created=None, updated=None):
        self.id = id
        self.title = title
        self.body = body
        self.created = created or datetime.now()
        self.updated = updated or self.created

    def __str__(self):
        return f"{self.title.upper()}\n{self.body}\nДата создания: {self.created}\nДата изменения: {self.updated}\n"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
        }
