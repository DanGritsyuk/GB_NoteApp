class PageData:
    def __init__(self, page_id: int, start_line_index: int, page_data: dict[str, list[str]], current_line_index = 0):
        self.page_id = page_id
        self.start_line_index = start_line_index
        self.current_line_index = current_line_index
        self.data = page_data.copy() if page_data != None else None
        self.lines_count = self._TasksCount()

    def _TasksCount(self):
        count = 0
        for key_work in self.data:
            count += len(self.data[key_work])
        return count