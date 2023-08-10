from View.ConsoleUI.ConsoleMenu import ConsoleMenu
from View.View import View


class ConsoleUI(View):
    def __init__(self):
        super().__init__()
        self.app_run = True

    def startup(self):
        while self.app_run:            
            self._draw_header()
            self._started_menu()

    def show_notes(self, notes):
        print(self.presenter.select_note(notes))
        input()

    def get_command(self):
        return input('Enter command: ')

    def ask_note_data(self) -> (str, str):
        title = input('Введите заголовок заметки: ')
        body = input('Введите текст заметки: ')
        return title, body

    def ask_note_id(self, notes) -> int:
        return ConsoleMenu.content_menu(notes, 'ЗАМЕТКИ:')

    def _started_menu(self):
        menu_data = {'ГЛАВНОЕ МЕНЮ:': ['СОЗДАТЬ', 'НАЙТИ', 'ПРОСМОТР'], '-------': ['ВЫХОД']}
        menu = ConsoleMenu(
            menu_data,
            f1=self._create_note,
            f2=self._method_stub,
            f3=self._show_notes,
            f_end=self._app_close,
        )
        menu.selected_menu()

    def _draw_header(self):
        ConsoleMenu.console_clear()
        print('ЗАМЕТКИ\n=======================================================================\n')

    def _create_note(self):
        self._draw_header()
        self.presenter.run_command('add')

    def _show_notes(self):
        self._draw_header()
        self.presenter.run_command('list')
    
    def _app_close(self):
        if ConsoleMenu.yesno_dialog('Завершить работу программы?'):
            ConsoleMenu.console_clear()
            print('Программа закрыта.')
            self.app_run = False
            return True

    def _method_stub(self):
        print('Функция в разработке...')
        input('Нажмите Enter ↵ ')
        self._draw_header()
