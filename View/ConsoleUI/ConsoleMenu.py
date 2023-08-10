import os
from View.ConsoleUI.MenuRender.MenuRender import MenuRender


class ConsoleMenu:
    CONSOLE_LINES = 12

    def __init__():
        pass

    def __init__(
        self,
        menu_data,
        f_end,
        f1=None,
        f2=None,
        f3=None,
        f4=None,
        f5=None,
        f6=None,
        f7=None,
        f8=None,
        f9=None,
        f10=None,
    ):
        self.runMenu = True
        self.menu_data = menu_data
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3
        self.f4 = f4
        self.f5 = f5
        self.f6 = f6
        self.f7 = f7
        self.f8 = f8
        self.f9 = f9
        self.f10 = f10
        self.f_end = f_end

    def selected_menu(self):
        def run_command(f, _f_end):
            close_menu = False
            if f is not None:
                close_menu = f()
            else:
                close_menu = _f_end()
            if close_menu:
                self.close_menu()

        commandKey = 1
        self.open_menu()
        while self.runMenu:
            commandKey = self._draw_menu(
                self.menu_data, 1 if commandKey == 0 else commandKey, self.CONSOLE_LINES
            )
            match commandKey:
                case 1:
                    run_command(self.f1, self.f_end)
                case 2:
                    run_command(self.f2, self.f_end)
                case 3:
                    run_command(self.f3, self.f_end)
                case 4:
                    run_command(self.f4, self.f_end)
                case 5:
                    run_command(self.f5, self.f_end)
                case 6:
                    run_command(self.f6, self.f_end)
                case 7:
                    run_command(self.f7, self.f_end)
                case 8:
                    run_command(self.f8, self.f_end)
                case 9:
                    run_command(self.f9, self.f_end)
                case 10:
                    run_command(self.f10, self.f_end)
                case _:
                    if self.f_end():
                        self.close_menu()

    def open_menu(self):
        self.runMenu = True

    def close_menu(self):
        self.runMenu = False

    @staticmethod
    def content_menu(items_menu, headerText):
        menuData = {}
        namesOnPage = []
        pageNumber = 0
        for name in items_menu:
            namesOnPage.append(name)
            if len(namesOnPage) >= ConsoleMenu.CONSOLE_LINES - 3 or len(
                namesOnPage
            ) + pageNumber * 10 == len(items_menu):
                menuData[headerText + " " + str(pageNumber + 1) + ":"] = namesOnPage
                namesOnPage = []
                pageNumber += 1
        return ConsoleMenu._draw_menu(menuData, 1,  ConsoleMenu.CONSOLE_LINES) - 1

    @staticmethod
    def console_clear():
        os.system("cls")

    @staticmethod
    def yesno_and_cancel_dialog(message):
        menuData = {message: ["Да", "Нет", "Отмена"]}
        return ConsoleMenu._draw_dialog_menu(menuData, 0)

    @staticmethod
    def yesno_dialog(message) -> bool:
        menuData = {message: ["Да", "Нет"]}
        commandKey = ConsoleMenu._draw_dialog_menu(menuData, 1)
        return commandKey == 1

    @staticmethod
    def _draw_menu(menuData, taskId, console_lines):
        return MenuRender.StartRenderMenu(
            menuData, taskId - 1, console_lines, True, True
        )

    @staticmethod
    def _draw_dialog_menu(menuData, taskIndex):
        return MenuRender.StartRenderMenu(menuData, taskIndex, 0, False, False)
