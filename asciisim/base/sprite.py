from abc import abstractmethod

from .game_object import GameObject

class AbstractSprite(GameObject):    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def update(self, context) -> None:
        pass        
