from abc import ABC, abstractmethod

class SpritePosition

class AbstractSprite(ABC):
    def __init__(self):
        self.image = None
        self.position = None

    @abstractmethod
    def update(self):
        pass
