
from datetime import datetime
import json

from Model.Notes.Note import Note


class NotesList:
    def __init__(self):
        self.filename = "notes.json"
        self.notes = []
        self.load()

    def load(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                for note_data in data:
                    note = Note(
                        id=note_data["id"],
                        title=note_data["title"],
                        body=note_data["body"],
                        created=datetime.fromisoformat(note_data["created"]),
                        updated=datetime.fromisoformat(note_data["updated"]),
                    )
                    self.notes.append(note)
        except FileNotFoundError:
            pass

    def save(self):
        data = [note.to_dict() for note in self.notes]
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def add_note(self, title, body):
        id = len(self.notes) + 1
        note = Note(id=id, title=title, body=body)
        self.notes.append(note)
        self.save()

    def get_id_and_titles(self) -> list[tuple[int, str]]:
        return [(note.id, note.title) for note in self.notes]

    def get_note_by_id(self, id):
        for note in self.notes:
            if note.id == id:
                return note
        return None

    def update_note_by_id(self, id, title=None, body=None):
        note = self.get_note_by_id(id)
        if note:
            note.title = title or note.title
            note.body = body or note.body
            note.updated = datetime.now()
            self.save()

    def delete_note_by_id(self, id):
        note = self.get_note_by_id(id)
        if note:
            self.notes.remove(note)
            self.save()