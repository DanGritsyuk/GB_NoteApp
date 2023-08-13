from datetime import datetime
import json
import os
from Model.Notes.Comporators.NoteComparatorByUpdateDate import NoteComparatorByUpdateDate
from Model.Notes.JsonFileHandler import JsonFileHandler

from Model.Notes.Note import Note


class NotesList:
    def __init__(self):
        self.filename = "Data\\notes.json"
        self.notes : list[Note] = []
        self.load()

    def load(self):
        data = JsonFileHandler.load(self.filename)
        if data != None:
            for note_data in data:
                note = Note(
                    id=note_data["id"],
                    title=note_data["title"],
                    body=note_data["body"],
                    created=datetime.fromisoformat(note_data["created"]),
                    updated=datetime.fromisoformat(note_data["updated"]),
                )
                self.notes.append(note)

    def save(self):
        data = [note.to_dict() for note in self.notes]
        JsonFileHandler.save(self.filename, data)

    def add_note(self, title, body):
        id = len(self.notes) + 1
        note = Note(id=id, title=title, body=body)
        self.notes.append(note)
        self.save()

    def get_notes_data_for_menu(self) -> list[tuple[int, str]]:
        return [(note.id, f'{note.updated.date()}: {note.title}') for note in self.notes]

    def get_note_by_id(self, id) -> Note:
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

    def sort_by_updated_date(self):
        self.notes.sort(key=NoteComparatorByUpdateDate.compare_notes_by_updated_date, reverse=True)