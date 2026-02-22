from abc import ABC, abstractmethod


class Listener(ABC):
    def action(self, node):
        return node

    @abstractmethod
    def entry(self, node):
        pass

    @abstractmethod
    def exit(self, node):
        pass
