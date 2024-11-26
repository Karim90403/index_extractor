from abc import ABC, abstractmethod


class ABCCommand(ABC):
    @abstractmethod
    def execute(self):
        ...

    @abstractmethod
    def add_arguments(self):
        ...

    @abstractmethod
    def set_arguments(self):
        ...
