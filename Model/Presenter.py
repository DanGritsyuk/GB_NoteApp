from Model.Notes.NotesList import NotesList
from Model.Notes.Note import Note
from View.View import View


class Presenter:
    def __init__(self, view: View):
        self.model = NotesList()
        self.view = view

    def run_command(self, command: str):
        if command == "list":
            self.view.show_notes(self.model.notes.__str__())
        elif command == "add":
            title, body = self.view.ask_note_data()
            self.model.add_note(title, body)
        elif command == "update":
            id = self.view.ask_note_id(self.model.notes)
            title, body = self.view.ask_note_data()
            self.model.update_note_by_id(id, title, body)
        elif command == "delete":
            id = self.view.ask_note_id()
            self.model.delete_note_by_id(id)

    def select_note(self):
        notes_titles = self.model.get_id_and_titles()
        id = self.view.ask_note_id(notes_titles)
        return self.model.get_note_by_id(id).__str__()