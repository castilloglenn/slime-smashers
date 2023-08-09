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

        if self.move_left:
            state.append("  Movement: LEFT")
        elif self.move_right:
            state.append("  Movement: RIGHT")
        else:
            state.append("  Movement:")

        if self.attack:
            state.append("  Action: ATTACK")
        elif self.defend:
            state.append("  Action: DEFEND")
        else:
            state.append("  Action:")

        if self.jump_up:
            state.append("  Special: JUMP UP")
        elif self.dash:
            state.append("  Special: DASH")
        else:
            state.append("  Special:")

        return state
