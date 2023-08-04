from dataclasses import dataclass
from typing import *

from absl import flags

FLAGS = flags.FLAGS


@dataclass
class ActionState:
    move_left = 0
    move_right = 0
    jump_up = 0
    jump_down = 0

    aim_left = 0
    aim_right = 0
    aim_up = 0
    aim_down = 0

    dash = 0
    attack = 0
    defend = 0

    @property
    def is_moving(self) -> bool:
        return any([self.move_left, self.move_right])

    @property
    def is_jumping(self) -> bool:
        return any([self.jump_up, self.jump_down])

    def __str__(self):
        actions = ""
        for attr in dir(self):
            if attr.startswith("__"):
                continue

            value = getattr(self, attr)
            if value > 0:
                actions += f"{attr}:{value:.2f}, "

        return f"{self.__class__.__name__}({actions[:-2]})"
