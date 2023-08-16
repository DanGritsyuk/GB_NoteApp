from Model.Notes.NotesList import NotesList
from View.View import View


class Presenter:
    def __init__(self, view: View):
        self.model = NotesList()
        self.view = view

    def run_command(self, command: str):
        if command == "list":
            self.view.show_notes()
        elif command == "add":
            title, body = self.view.ask_note_data()
            self.model.add_note(title, body)
        elif command == "update":
            id = self.view.ask_note_id(self.model.get_notes_data_for_menu())
            title, body = self.view.ask_note_data()
            self.model.update_note_by_id(id, title, body)
        elif command == "delete":
            id = self.view.ask_note_id(self.model.get_notes_data_for_menu())
            self.model.delete_note_by_id(id)
        else:
            self.view.show_message('Недопустимая команда')

    def select_note(self):
        self.model.sort_by_updated_date()
        notes_titles = self.model.get_notes_data_for_menu()
        if len(notes_titles) == 0:
            self.view.show_message('Список заметок пуст.')
        else:
            id = self.view.ask_note_id(notes_titles)
            if id != None:
                return self.model.get_note_by_id(id).__str__()