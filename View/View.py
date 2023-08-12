from abc import ABC, abstractmethod



class View(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def show_notes(self, notes):
        pass

    @abstractmethod
    def ask_note_data(self) -> (str, str):
        pass

    @abstractmethod
    def ask_note_id(self, notes) -> int:
        pass

    @abstractmethod
    def show_message(self, message: str):
        pass