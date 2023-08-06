class PageData:
    def __init__(self, pageId: int, startLineIndex: int, pageData: dict[str, list[str]], currentLineIndex = 0):
        self.pageId = pageId
        self.startLineIndex = startLineIndex
        self.currentLineIndex = currentLineIndex
        self.pageData = pageData.copy() if pageData != None else None
        self.linesCount = self._TasksCount()

    def _TasksCount(self):
        count = 0
        for keyWork in self.pageData:
            count += len(self.pageData[keyWork])
        return count