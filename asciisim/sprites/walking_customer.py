from .abstract_customer import AbstractCustomer
from .sprite_enums import CustomerStatus


class WalkingCustomer(AbstractCustomer):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, status=CustomerStatus.WALKING)
