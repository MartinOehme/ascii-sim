from abc import abstractmethod

from .context import Context
from .game_object import GameObject

class AbstractSprite(GameObject):    
    def __init__(self):
        self.position = None

    @abstractmethod
    def update(self, context: Context) -> None:
        pass        
