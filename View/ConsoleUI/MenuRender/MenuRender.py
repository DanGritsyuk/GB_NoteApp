from typing import List

from View.ConsoleUI.MenuRender.ConsoleManager import ConsoleManager
from View.ConsoleUI.MenuRender.PageData import PageData
from View.ConsoleUI.MenuRender.Point2D import Point2D


class MenuRender:
    
    HEADER_LINE_COUNT = 2
    LINE_MAX_CHARACTER_COUNT = 190

    @staticmethod
    def start_render_memu(
        menu_data: dict[str, list[str]],
        index: int = 0,
        console_lines: int = 0,
        is_esc_active: bool = False,
        show_help_control: bool = False,
        prefix: str = "> ",
        prefix_mark: str = "",
    ) -> int:

        largest_key = MenuRender._largest_key_tasks(menu_data) + MenuRender.HEADER_LINE_COUNT + 1
        console_lines = largest_key + 1 if largest_key > console_lines else console_lines

        def start_draw():
            MenuRender._draw_menu(
                page,
                page_count,
                cursor_start_position,
                console_lines,
                show_help_control,
                prefix,
                prefix_mark,
            )

        def get_next_page(_page: PageData, step: int) -> PageData:
            ConsoleManager.set_cursor_position(cursor_start_position)
            MenuRender._clear_console_text(
                MenuRender._get_largest_line_length(_page.data, len(prefix), len(prefix_mark)) + len(prefix),
                console_lines,
            )
            current_index = _page.current_line_index
            _page = list(filter(lambda p: p.page_id == _page.page_id + step, pages_map))[0]
            _page.current_line_index = (
                current_index
                if current_index < _page.lines_count
                else _page.lines_count - 1
            )
            return _page

        def get_check_coordinates() -> PageData:
            for page in pages_map:
                if page.start_line_index <= index < page.start_line_index + page.lines_count:
                    page.current_line_index = index - page.start_line_index
                    return page
            raise Exception("Page not found!")

        def _end_draw(_page: PageData):
            ConsoleManager.hide_cursor(False)
            ConsoleManager.set_cursor_position(cursor_start_position)
            MenuRender._clear_console_text(
                MenuRender._get_largest_line_length(_page.data, len(prefix), len(prefix_mark)) + len(prefix),
                console_lines,
            )
            ConsoleManager.set_cursor_position(cursor_start_position)

        pages_map = MenuRender._split_data_to_pages(
            menu_data, console_lines, MenuRender.HEADER_LINE_COUNT
        )
        page = get_check_coordinates()
        page_count = len(pages_map)

        cursor_start_position = ConsoleManager.get_cursor_coordinate()
        start_draw()
        while True:
            ConsoleManager.hide_cursor(True)
            key = ConsoleManager.get_key_event()
            match key:
                case "enter":
                    _end_draw(page)
                    return page.current_line_index + page.start_line_index + 1
                case "up":
                    if page.current_line_index > 0:
                        page.current_line_index -= 1
                case "down":
                    if page.current_line_index < MenuRender._LineCount(page.data) - 1:
                        page.current_line_index += 1
                case "left":
                    if page.page_id > 1:
                        page = get_next_page(page, -1)
                case "rigth":
                    if page.page_id < page_count:
                        page = get_next_page(page, 1)
                case "esc":
                    if is_esc_active:
                        _end_draw(page)
                        return 0
            start_draw()

    @staticmethod
    def _split_data_to_pages(
        menu_data: dict[str, list[str]], lines_dage: int, header_line_count: int
    ) -> set():
        page_line_count = 0
        page_first_index = 0
        page_id = 1
        page_data = dict()
        pages_map = set()
        for i, key in enumerate(menu_data):
            count_lines_key_tasks = len(menu_data[key])
            if count_lines_key_tasks + header_line_count + page_line_count >= lines_dage:
                page = PageData(page_id, page_first_index, page_data)
                pages_map.add(page)
                page_line_count = 0
                page_id += 1
                page_first_index += page.lines_count
                page_data.clear()
            page_line_count += count_lines_key_tasks + 2
            page_data[key] = menu_data[key]
            if i == len(menu_data) - 1:
                pages_map.add(PageData(page_id, page_first_index, page_data))
        return pages_map

    @staticmethod
    def _draw_menu(
        page: PageData,
        pages_count: int,
        cursor_start_position: Point2D,
        lines_count: int,
        show_help_control: bool,
        prefix: str,
        prefix_mark: str,
    ):
        def short_menu_line(line) -> str:
                if len(line) > MenuRender.LINE_MAX_CHARACTER_COUNT:
                    return line[:MenuRender.LINE_MAX_CHARACTER_COUNT-3] + "..."
                return line
        ConsoleManager.set_cursor_position(cursor_start_position)
        block_id_count = 0
        largest_line = int(MenuRender._get_largest_line_length(page.data, len(prefix), len(prefix_mark)))
        for key in page.data:
            if block_id_count > 0:
                print()
            print(short_menu_line(key))
            for i, line in enumerate(page.data[key]):
                print_to_console = ''
                i += block_id_count
                is_selected = i == page.current_line_index
                if is_selected:
                    MenuRender._clear_line_text(largest_line)
                if prefix_mark == "":
                    print_to_console = prefix if is_selected else str(" " * len(prefix))
                    print_to_console = f"{print_to_console}{line}"
                else:
                    print_to_console = (
                        line.replace(prefix_mark, prefix)
                        if is_selected
                        else line.replace(prefix_mark, str(" " * len(prefix_mark)))
                    )
                print(short_menu_line(print_to_console))
            block_id_count += len(page.data[key])
        if show_help_control:
            str_page_numbers = ""
            if pages_count > 1:
                str_page_numbers = "▪" * pages_count
                string_page_id = str(page.page_id)
                for i in range(len(string_page_id)):
                    str_page_numbers = (
                        str_page_numbers[: page.page_id - 1 + i]
                        + string_page_id[i]
                        + str_page_numbers[page.page_id + i :]
                    )
            indent = " " * 50
            if pages_count > 2:
                if page.page_id > 1:
                    str_page_numbers = "← " + str_page_numbers
                else:
                    str_page_numbers = "  " + str_page_numbers
                if page.page_id < pages_count:
                    str_page_numbers = str_page_numbers + " →"
                else:
                    str_page_numbers = str_page_numbers + "  "
            print(
                "\n" * int(lines_count - page.lines_count - len(page.data) * 2),
                end=f"{indent}{str_page_numbers}\n",
            )

            padding = "=" * largest_line
            pages_switch_info = "← → - переключать страницы. " if pages_count > 1 else ""
            print(
                f"{padding}\n↑ ↓ - перемещаться между строками. {pages_switch_info}Enter - выбрать задачу. Для выхода нажмите Esc."
            )
        print()

    @staticmethod
    def _LineCount(menu_data: dict[str, list[str]]):
        count = 0
        for key in menu_data:
            count += len(menu_data[key])
        return count

    @staticmethod
    def _get_largest_line_length(menu_data: dict[str, list[str]], len_peffix: int, len_prefix_mark: int) -> int:
        larges_line_length = 0
        for key, value in menu_data.items():
            len_key = len(key)
            if larges_line_length < len_key:
                larges_line_length == len_key
            if not isinstance(value, list) or not all(isinstance(line, str) for line in value):
                continue
            max_length = max([len(line) for line in value])
            max_length += len_peffix if len_peffix > len_prefix_mark else len_prefix_mark
            if larges_line_length < max_length:
                larges_line_length = max_length
        return larges_line_length if larges_line_length > MenuRender.LINE_MAX_CHARACTER_COUNT else MenuRender.LINE_MAX_CHARACTER_COUNT

    @staticmethod
    def _largest_key_tasks(menu_data: dict[str, list[str]]) -> int:
        larges_key__tasks = 0
        for key in menu_data:
            length_key_tasks = len(menu_data[key])
            larges_key__tasks = (
                length_key_tasks if length_key_tasks > larges_key__tasks else larges_key__tasks
            )
        return larges_key__tasks

    @staticmethod
    def _clear_console_text(chars_count: int, lines_count: int):
        for _ in range(lines_count):
            print(" " * chars_count)

    @staticmethod
    def _clear_line_text(line_count: int):
        point_cursor = ConsoleManager.get_cursor_coordinate()
        print(" " * line_count)
        ConsoleManager.set_cursor_position(point_cursor)
