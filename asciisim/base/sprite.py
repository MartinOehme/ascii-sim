from abc import ABC, abstractmethod

class AbstractSprite(ABC):
    def __init__(self):
        self.image = None
        self.position = None

    @abstractmethod
    def update(self):
        pass

