from abc import ABC, abstractmethod


class Listener(ABC):
    @abstractmethod
    def action(self, node):
        pass

    @abstractmethod
    def entry(self, node):
        pass

    @abstractmethod
    def exit(self, node):
        pass
