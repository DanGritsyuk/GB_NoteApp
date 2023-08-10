from Model.Notes.NotesList import NotesList


class Presenter:
    def __init__(self, view):
        self.model = NotesList()
        self.view = view
        pass

    def run_command(self, command):
        if command == "list":
            self.view.show_notes(self.model.notes)
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

    def select_note(self, notes):
        notes_titls = []
        for note in notes:
            notes_titls.append(note.title)
        index = self.view.ask_note_id(notes_titls)
        return notes[index].__str__()