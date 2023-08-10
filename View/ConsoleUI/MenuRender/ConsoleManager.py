import os
import sys
import msvcrt
import ctypes
from View.ConsoleUI.MenuRender.Point2D import Point2D

class ConsoleManager:

    @staticmethod
    def GetCursorCoordinate() -> Point2D:
        print('\033[A\033[6n')
        buff = ''

        def DelWeedSymbols(line: str) -> str:
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

        newbuff = DelWeedSymbols(buff.replace('\x1b[', ''))

        return Point2D(
            int(newbuff.partition(';')[2]),
            int(newbuff.partition(';')[0]),
        )

    @staticmethod
    def SetCursorPosition(toPosition: Point2D):
        correntPosition = ConsoleManager.GetCursorCoordinate()

        yDistance = correntPosition.y - toPosition.y
        if yDistance > 0:
            print('\033[A' * yDistance, end='')

        xDistance = correntPosition.x - toPosition.x
        if xDistance > 0:
            print('\033[D' * xDistance, end='')

    @staticmethod
    def GetKeyEvent() -> str:
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
    def PrintASCIIText(text: str):
        print(text)

    @staticmethod
    def HideCursor(isHidden: bool) -> str:
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