from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def CheckParameters(self):
        pass

    @abstractmethod
    def Execute(self):
        pass