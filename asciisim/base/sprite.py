from abc import ABC, abstractmethod

from .context import Context

class AbstractSprite(ABC):
    def __init__(self):
        self.image = None
        self.position = None

    @abstractmethod
    def update(self, context: Context):
        pass

