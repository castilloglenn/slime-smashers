from dataclasses import dataclass
from typing import *

from absl import flags
from pygame import Vector2

from src.util.logger import TextLogger
from src.util.state import ActionState
from src.util.types import PixelPerSec

FLAGS = flags.FLAGS


@dataclass
class Motion:
    gravity_: PixelPerSec
    ms: PixelPerSec

    LEFT: int = 0
    RIGHT: int = 1

    def __post_init__(self):
        self.gravity = Vector2(0, self.gravity_)
        self.ms_amp = 1.0

        self.on_ground = False
        self.move_lock = None

        self.last_facing = Motion.RIGHT

    @staticmethod
    def preload(text_logger: TextLogger):
        text_logger.preload("Motion")

        categories = {
            "Speed": ["NORMAL", "SLOWED"],
            "Gravity": ["NORMAL"],
            "On-Ground": ["TRUE", "FALSE"],
            "Lock": ["LEFT", "RIGHT"],
        }
        text_logger.preload_dict(categories=categories)

    @property
    def right_turn(self) -> bool:
        return self.last_facing == Motion.RIGHT

    @property
    def is_move_locked(self) -> bool:
        return self.move_lock is not None

    @property
    def speed(self) -> float:
        return self.ms * self.ms_amp

    def text_log(self, text_logger: TextLogger):
        text_logger.add("Motion")

        text_logger.decide(
            category="Speed",
            values=["NORMAL", "SLOWED"],
            conditions=[self.ms_amp == 1.0, self.ms_amp < 1.0],
        )

        text_logger.add("Gravity: NORMAL")

        text_logger.decide(
            category="On-Ground",
            values=["TRUE", "FALSE"],
            conditions=[self.on_ground, not self.on_ground],
        )

        text_logger.decide(
            category="Lock",
            values=["LEFT", "RIGHT"],
            conditions=[
                self.move_lock == Motion.LEFT,
                self.move_lock == Motion.RIGHT,
            ],
        )

        text_logger.add_empty()

    def modify_move_lock(self, n: int):
        self.move_lock = n
        self.last_facing = n

    def modify_ms(self, n: float):
        self.ms_amp = n

    def get_descend(self, delta: float) -> Vector2:
        return self.gravity * delta

    def get_move(self, delta: float, action_state: ActionState) -> Vector2:
        move = Vector2(0, 0)

        left = action_state.move_left
        right = action_state.move_right
        if left and right or self.is_move_locked:
            return move

        if left:
            move = Vector2(-1, 0)
            self.last_facing = Motion.LEFT
        elif right:
            move = Vector2(1, 0)
            self.last_facing = Motion.RIGHT

        return move * self.speed * delta
