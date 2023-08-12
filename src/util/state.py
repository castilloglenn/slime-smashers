from dataclasses import dataclass
from typing import *

from absl import flags

from src.util.logger import TextLogger

FLAGS = flags.FLAGS


@dataclass
class ActionState:
    source: str
    
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

    @staticmethod
    def preload(text_logger: TextLogger):
        titles = ["Keyboard", "Joystick"]
        for t in titles:
            text_logger.preload(t)

        movement = ["LEFT", "RIGHT"]
        for m in movement:
            text_logger.preload(f"Movement: {m}", indented=True)

        action = ["ATTACK", "DEFEND"]
        for a in action:
            text_logger.preload(f"Action: {a}", indented=True)

        special = ["DASH", "JUMP UP"]
        for s in special:
            text_logger.preload(f"Special: {s}", indented=True)

    @property
    def is_moving(self) -> bool:
        return any([self.move_left, self.move_right])

    @property
    def is_jumping(self) -> bool:
        return any([self.jump_up, self.jump_down])
    
    def text_log(text_logger: TextLogger):
        
