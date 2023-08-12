import string
from Model.Presenter import Presenter
from View.View import View


class TextCommandUI(View):
    def startup(self):
        self.presenter = Presenter(self)
        self.print_help()
        while True:
            command = self.get_command()
            if command == "quit":
                break
            else:
                self.presenter.run_command(command)

    def show_notes(self):
        info = self.presenter.select_note()
        print(info)

    def get_command(self):
        return input("Введите комманду: ")

    def ask_note_data(self) -> (str, str):
        title = self._get_text("Введите заголовок заметки: ")
        body = self._get_text("Введите текст заметки: ")
        return title, body

    def ask_note_id(self, notes_info):
        for info in notes_info:
            print(f'ID: {info[0]} - {info[1]}')
        enterind_id = True
        while enterind_id:
            try:
                id = int(input("Введите id: "))
                enterind_id = False
                return id
            except:
                input('Недопустимое число')

    def show_message(self, message: str):
        input(message)

    @staticmethod
    def print_help():
        print('Комманды:\nlist - показать заметки\nadd - добавить новую заметку\nupdate - редактировать заметку\ndelete - удалить заметку\nquit - выход\n')

    @staticmethod
    def _get_text(message: str) -> str:
        entered = True
        while entered:
            text = input(message)
            if text != '':
                entered = False
            else:
                return TextCommandUI._get_text('Пустое поле не допустимо, повторите попытку: ')
        return text 