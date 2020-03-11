# Python Imports
import enum
# Third-Party Imports
# Project Imports


@enum.unique
class LoopModes(enum.Enum):

    NOT = 0
    QUEUE = 1
    ONE = 2

    def get_next_value(self):
        # noinspection PyTypeChecker
        return (self.value + 1) % len(LoopModes)

    def get_next_key(self):
        return LoopModes(self.get_next_value())
