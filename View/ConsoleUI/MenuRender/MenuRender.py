from typing import List

from View.ConsoleUI.MenuRender.ConsoleManager import ConsoleManager
from View.ConsoleUI.MenuRender.PageData import PageData
from View.ConsoleUI.MenuRender.Point2D import Point2D


class MenuRender:
    
    HEADER_LINE_COUNT = 2
    LINE_MAX_CHARACTER_COUNT = 190

    @staticmethod
    def start_render_memu(
        menuData: dict[str, list[str]],
        index: int = 0,
        consoleLines: int = 0,
        isEscActive: bool = False,
        showHelpControl: bool = False,
        prefix: str = "> ",
        prefixMark: str = "",
    ) -> int:

        largestKey = MenuRender._largest_key_tasks(menuData) + MenuRender.HEADER_LINE_COUNT + 1
        consoleLines = largestKey + 1 if largestKey > consoleLines else consoleLines

        def start_draw():
            MenuRender._draw_menu(
                page,
                pageCount,
                cursorStartPosition,
                consoleLines,
                showHelpControl,
                prefix,
                prefixMark,
            )

        def get_next_page(_page: PageData, step: int) -> PageData:
            ConsoleManager.set_cursor_position(cursorStartPosition)
            MenuRender._clear_console_text(
                MenuRender._get_largest_line_length(_page.pageData, len(prefix), len(prefixMark)) + len(prefix),
                consoleLines,
            )
            currentIndex = _page.currentLineIndex
            _page = list(filter(lambda p: p.pageId == _page.pageId + step, pagesMap))[0]
            _page.currentLineIndex = (
                currentIndex
                if currentIndex < _page.linesCount
                else _page.linesCount - 1
            )
            return _page

        def get_check_coordinates() -> PageData:
            for page in pagesMap:
                if page.startLineIndex <= index < page.startLineIndex + page.linesCount:
                    page.currentLineIndex = index - page.startLineIndex
                    return page
            raise Exception("Page not found!")

        def _end_draw(_page: PageData):
            ConsoleManager.hide_cursor(False)
            ConsoleManager.set_cursor_position(cursorStartPosition)
            MenuRender._clear_console_text(
                MenuRender._get_largest_line_length(_page.pageData, len(prefix), len(prefixMark)) + len(prefix),
                consoleLines,
            )
            ConsoleManager.set_cursor_position(cursorStartPosition)

        pagesMap = MenuRender._split_data_to_pages(
            menuData, consoleLines, MenuRender.HEADER_LINE_COUNT
        )
        page = get_check_coordinates()
        pageCount = len(pagesMap)

        cursorStartPosition = ConsoleManager.get_cursor_coordinate()
        start_draw()
        while True:
            ConsoleManager.hide_cursor(True)
            key = ConsoleManager.GetKeyEvent()
            match key:
                case "enter":
                    _end_draw(page)
                    return page.currentLineIndex + page.startLineIndex + 1
                case "up":
                    if page.currentLineIndex > 0:
                        page.currentLineIndex -= 1
                case "down":
                    if page.currentLineIndex < MenuRender._LineCount(page.pageData) - 1:
                        page.currentLineIndex += 1
                case "left":
                    if page.pageId > 1:
                        page = get_next_page(page, -1)
                case "rigth":
                    if page.pageId < pageCount:
                        page = get_next_page(page, 1)
                case "esc":
                    if isEscActive:
                        _end_draw(page)
                        return 0
            start_draw()

    @staticmethod
    def _split_data_to_pages(
        menuData: dict[str, list[str]], linesPage: int, headerLineCount: int
    ) -> set():
        pageLineCount = 0
        pageFirstIndex = 0
        pageId = 1
        pageData = dict()
        pagesMap = set()
        for i, key in enumerate(menuData):
            countLinesKeyTasks = len(menuData[key])
            if countLinesKeyTasks + headerLineCount + pageLineCount >= linesPage:
                page = PageData(pageId, pageFirstIndex, pageData)
                pagesMap.add(page)
                pageLineCount = 0
                pageId += 1
                pageFirstIndex += page.linesCount
                pageData.clear()
            pageLineCount += countLinesKeyTasks + 2
            pageData[key] = menuData[key]
            if i == len(menuData) - 1:
                pagesMap.add(PageData(pageId, pageFirstIndex, pageData))
        return pagesMap

    @staticmethod
    def _draw_menu(
        page: PageData,
        pagesCount: int,
        cursorStartPosition: Point2D,
        linesCount: int,
        showHelpControl: bool,
        prefix: str,
        prefixMark: str,
    ):
        def shortMenuLine(line) -> str:
                if len(line) > MenuRender.LINE_MAX_CHARACTER_COUNT:
                    return line[:MenuRender.LINE_MAX_CHARACTER_COUNT-3] + "..."
                return line
        ConsoleManager.set_cursor_position(cursorStartPosition)
        blockIdCount = 0
        largestLine = int(MenuRender._get_largest_line_length(page.pageData, len(prefix), len(prefixMark)))
        for key in page.pageData:
            if blockIdCount > 0:
                print()
            print(shortMenuLine(key))
            for i, line in enumerate(page.pageData[key]):
                prToConsole = ''
                i += blockIdCount
                isSelected = i == page.currentLineIndex
                if isSelected:
                    MenuRender._clear_line_text(largestLine)
                if prefixMark == "":
                    prToConsole = prefix if isSelected else str(" " * len(prefix))
                    prToConsole = f"{prToConsole}{line}"
                else:
                    prToConsole = (
                        line.replace(prefixMark, prefix)
                        if isSelected
                        else line.replace(prefixMark, str(" " * len(prefixMark)))
                    )
                print(shortMenuLine(prToConsole))
            blockIdCount += len(page.pageData[key])
        if showHelpControl:
            strPageNumbers = ""
            if pagesCount > 1:
                strPageNumbers = "▪" * pagesCount
                strPageId = str(page.pageId)
                for i in range(len(strPageId)):
                    strPageNumbers = (
                        strPageNumbers[: page.pageId - 1 + i]
                        + strPageId[i]
                        + strPageNumbers[page.pageId + i :]
                    )
            indent = " " * 50
            if pagesCount > 2:
                if page.pageId > 1:
                    strPageNumbers = "← " + strPageNumbers
                else:
                    strPageNumbers = "  " + strPageNumbers
                if page.pageId < pagesCount:
                    strPageNumbers = strPageNumbers + " →"
                else:
                    strPageNumbers = strPageNumbers + "  "
            print(
                "\n" * int(linesCount - page.linesCount - len(page.pageData) * 2),
                end=f"{indent}{strPageNumbers}\n",
            )

            padding = "=" * largestLine
            pagesSwitchInfo = "← → - переключать страницы. " if pagesCount > 1 else ""
            print(
                f"{padding}\n↑ ↓ - перемещаться между строками. {pagesSwitchInfo}Enter - выбрать задачу. Для выхода нажмите Esc."
            )
        print()

    @staticmethod
    def _LineCount(menuData: dict[str, list[str]]):
        count = 0
        for key in menuData:
            count += len(menuData[key])
        return count

    @staticmethod
    def _get_largest_line_length(menuData: dict[str, list[str]], lenPeffix: int, lenPrMark: int) -> int:
        largesLineLength = 0
        for key, value in menuData.items():
            len_key = len(key)
            if largesLineLength < len_key:
                largesLineLength == len_key
            if not isinstance(value, list) or not all(isinstance(line, str) for line in value):
                continue
            maxLength = max([len(line) for line in value])
            maxLength += lenPeffix if lenPeffix > lenPrMark else lenPrMark
            if largesLineLength < maxLength:
                largesLineLength = maxLength
        return largesLineLength if largesLineLength > MenuRender.LINE_MAX_CHARACTER_COUNT else MenuRender.LINE_MAX_CHARACTER_COUNT

    @staticmethod
    def _largest_key_tasks(menuData: dict[str, list[str]]) -> int:
        largesKeyTasks = 0
        for key in menuData:
            lengthKeyTasks = len(menuData[key])
            largesKeyTasks = (
                lengthKeyTasks if lengthKeyTasks > largesKeyTasks else largesKeyTasks
            )
        return largesKeyTasks

    @staticmethod
    def _clear_console_text(charsCount: int, linesCount: int):
        for _ in range(linesCount):
            print(" " * charsCount)

    @staticmethod
    def _clear_line_text(lineCount: int):
        pointCursor = ConsoleManager.get_cursor_coordinate()
        print(" " * lineCount)
        ConsoleManager.set_cursor_position(pointCursor)
