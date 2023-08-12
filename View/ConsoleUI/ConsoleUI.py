from Model.Presenter import Presenter
from View.ConsoleUI.ConsoleMenu import ConsoleMenu
from View.View import View


class ConsoleUI(View):
    def __init__(self):
        super().__init__()
        self.presenter = Presenter(self)
        self.app_run = True
        self.last_index_selected_note = 0
        self.selected_note_id = None

    def startup(self):
        while self.app_run:            
            self._draw_header()
            self._started_menu()

    def show_notes(self):
        selecting_note = True
        while selecting_note:
            self._draw_header()
            note_data = self.presenter.select_note()
            if note_data != None:
                print(note_data)
                menuData = {' ': ['Редактировать', 'Удалить', 'Назад']}
                task_id = ConsoleMenu.draw_dialog_menu(menuData, 0)
                if task_id == 1:
                    command = self.presenter.run_command('update')
                elif task_id == 2: 
                    if ConsoleMenu.yesno_dialog('Удалить заметку?'):
                        command = self.presenter.run_command('delete')
                        self.selected_note_id = None
                else:
                    self.selected_note_id = None
            else:
                selecting_note = False
        self.selected_note_id = None
        self.last_index_selected_note = 0

    def ask_note_data(self) -> (str, str):
        title = self._get_text('Введите заголовок заметки: ')
        body = self._get_text('Введите текст заметки: ')
        return title, body

    def ask_note_id(self, data: list[tuple[int, str]]) -> int:
        if self.selected_note_id != None:
            return self.selected_note_id
        menu_lines = []
        for item in data:
            menu_lines.append(item[1])
        index = ConsoleMenu.content_menu(menu_lines, 'ЗАМЕТКИ', self.last_index_selected_note)
        if index >= 0:
            self.last_index_selected_note = index
            self.selected_note_id = data[index][0]
            return self.selected_note_id
    
    def show_message(self, message: str):
        self._draw_header()
        print(message)
        input('Нажмите Enter ↵ ')

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
        print('=' * ConsoleMenu.get_max_characters_line(), end='\n\n')

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
    
    @staticmethod
    def _get_text(message: str) -> str:
        entered = True
        while entered:
            text = input(message)
            if text != '':
                entered = False
            else:
                ConsoleUI._clear_line()
                input('Пустое поле не допустимо...      ')
                ConsoleUI._clear_line()
        return text        
    
    @staticmethod
    def _clear_line():
        print('\033[A', end='')
        print(' ' * ConsoleMenu.get_max_characters_line(), end='')
        print('\b' * ConsoleMenu.get_max_characters_line(), end='')

    def _method_stub(self):
        self.show_message('Функция в разработке...')
        self._draw_header()
