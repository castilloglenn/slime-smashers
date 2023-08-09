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

    @property
    def text_state(self) -> list[str]:
        state = []

        movement = "  Movement: "
        if self.move_left:
            movement += "LEFT"
        elif self.move_right:
            movement += "RIGHT"
        state.append(movement)

        action = "  Action: "
        if self.attack:
            action += "ATTACK"
        elif self.defend:
            action += "DEFEND"
        state.append(action)

        special = "  Special: "
        if self.jump_up:
            special += "JUMP UP"
        elif self.dash:
            special += "DASH"
        state.append(special)

        return state
