from dataclasses import dataclass
from typing import *

from absl import flags

from src.util.logger import KEYPAIR_FMT, TextLogger

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
        titles = ["Keyboard", "Joystick", "Joystick (Disconnected)"]
        for t in titles:
            text_logger.preload(t)

        categories = {
            "Movement": ["LEFT", "RIGHT"],
            "Action": ["ATTACK", "DEFEND"],
            "Special": ["DASH", "JUMP UP"],
        }
        text_logger.preload_dict(categories=categories)

    @property
    def is_moving(self) -> bool:
        return any([self.move_left, self.move_right])

    @property
    def is_jumping(self) -> bool:
        return any([self.jump_up, self.jump_down])

    def text_log(self, text_logger: TextLogger):
        text_logger.add(self.source)

        text_logger.decide(
            category="Movement",
            values=["LEFT", "RIGHT"],
            conditions=[self.move_left, self.move_right],
        )

        text_logger.decide(
            category="Action",
            values=["ATTACK", "DEFEND"],
            conditions=[self.attack, self.defend],
        )

        text_logger.decide(
            category="Special",
            values=["JUMP UP", "DASH"],
            conditions=[self.jump_up, self.dash],
        )
