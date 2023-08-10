from abc import ABC, abstractmethod
from Model.Presenter import Presenter


class View(ABC):
    def __init__(self):
        self.presenter = Presenter(self)
        pass

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def show_notes(self, notes):
        pass

    @abstractmethod
    def get_command(self):
        pass

    @abstractmethod
    def ask_note_data(self) -> (str, str):
        pass

    @abstractmethod
    def ask_note_id(self, notes) -> int:
        pass