from Model.Presenter import Presenter
from View.ConsoleUI.ConsoleMenu import ConsoleMenu
from View.View import View


class ConsoleUI(View):
    def __init__(self):
        super().__init__()
        self.presenter = Presenter(self)
        self.app_run = True

    def startup(self):
        while self.app_run:            
            self._draw_header()
            self._started_menu()

    def show_notes(self, info: str):
        print(self.presenter.select_note())
        input()

    def get_command(self):
        return input('Enter command: ')

    def ask_note_data(self) -> (str, str):
        title = input('Введите заголовок заметки: ')
        body = input('Введите текст заметки: ')
        return title, body

    def ask_note_id(self, data: list[tuple[int, str]]) -> int:
        menu_lines = [str]
        for item in data:
            menu_lines.append(item[1])
        index = ConsoleMenu.content_menu(menu_lines, 'ЗАМЕТКИ')
        if index >= 0:
            return data[index][0]

    def _started_menu(self):
        menu_data = {'ГЛАВНОЕ МЕНЮ:': ['НОВАЯ ЗАМЕТКА', 'НАЙТИ ЗАМЕТКУ', 'ВСЕ ЗАМЕТКИ'], '-------': ['ВЫХОД']}
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
        print('ЗАПИСНАЯ КНИГА')
        print('=' * 190, end='\n\n')

    def _create_note(self):
        self._run_command('add')

    def _show_notes(self):
        self._run_command('list')
    
    def _app_close(self):
        if ConsoleMenu.yesno_dialog('Завершить работу программы?'):
            ConsoleMenu.console_clear()
            print('Программа закрыта.')
            self.app_run = False
            return True
        
    def _run_command(self, command: str):
        self._draw_header()
        self.presenter.run_command(command)
        self._draw_header()

    def _method_stub(self):
        print('Функция в разработке...')
        input('Нажмите Enter ↵ ')
        self._draw_header()
