import os
import sys
import msvcrt
import ctypes
from View.ConsoleUI.MenuRender.Point2D import Point2D

class ConsoleManager:

    @staticmethod
    def get_cursor_coordinate() -> Point2D:
        print('\033[A\033[6n')
        buff = ''

        def del_weed_symbols(line: str) -> str:
            first = 0
            if line[0] < '1' or line[0] > '9':
                first = 1
            for i, chr in enumerate(line):
                if chr == 'R':
                    return line[first:i]
            return line

        keep_going = True
        while keep_going:
            buff += msvcrt.getch().decode('ASCII')
            keep_going = msvcrt.kbhit()

        newbuff = del_weed_symbols(buff.replace('\x1b[', ''))

        return Point2D(
            int(newbuff.partition(';')[2]),
            int(newbuff.partition(';')[0]),
        )

    @staticmethod
    def set_cursor_position(to_position: Point2D):
        corrent_position = ConsoleManager.get_cursor_coordinate()

        y_distance = corrent_position.y - to_position.y
        if y_distance > 0:
            print('\033[A' * y_distance, end='')

        x_distance = corrent_position.x - to_position.x
        if x_distance > 0:
            print('\033[D' * x_distance, end='')

    @staticmethod
    def get_key_event() -> str:
        match msvcrt.getch():
            case b'\r':
                return 'enter'
            case b'\x00':
                key = msvcrt.getch()
                if key == b'H':
                    return 'up'
                elif key == b'P':
                    return 'down'
                elif key == b'K':
                    return 'left'
                elif key == b'M':
                    return 'rigth'
            case b'\x1b':
                return 'esc'

    @staticmethod
    def print_ASCII_text(text: str):
        print(text)

    @staticmethod
    def hide_cursor(isHidden: bool) -> str:
        if os.name == 'nt':
            ci = _CursorInfo()
            handle = ctypes.windll.kernel32.GetStdHandle(-11)
            ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
            ci.visible = not isHidden
            ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
        elif os.name == 'posix':
            if isHidden:
                sys.stdout.write("\033[?25l")
            else:
                sys.stdout.write("\033[?25h")

class _CursorInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),
                ("visible", ctypes.c_byte)]