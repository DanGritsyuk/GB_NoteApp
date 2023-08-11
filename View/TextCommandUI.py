import string
from Model.Presenter import Presenter
from View.View import View


class TextCommandUI(View):
    def startup(self):
        self.presenter = Presenter(self)
        while True:
            command = self.get_command()
            if command == "quit":
                break
            else:
                self.presenter.run_command(command)

    def show_notes(self, notes):
        for note in notes:
            print(note)

    def get_command(self):
        return input("Enter command: ")

    def ask_note_data(self) -> (str, str):
        title = input("Enter title: ")
        body = input("Enter body: ")
        return title, body

    def ask_note_id(self, notes):
        self.show_notes(notes)
        return int(input("Enter note id: "))