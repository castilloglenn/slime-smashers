from dataclasses import dataclass
from typing import *

from absl import flags
from pygame import Vector2

from src.util.state import ActionState
from src.util.types import PixelPerSec

FLAGS = flags.FLAGS


@dataclass
class Motion:
    gravity_: PixelPerSec
    ms: PixelPerSec

    RIGHT: int = 0
    LEFT: int = 1

    def __post_init__(self):
        self.gravity = Vector2(0, self.gravity_)
        self.ms_amp = 1.0

        self.on_ground = False
        self.move_lock = None

        self.last_facing = None

    @property
    def is_facing_right(self) -> bool:
        return self.last_facing == Motion.RIGHT

    @property
    def is_move_locked(self) -> bool:
        return self.move_lock is not None

    def modify_move_lock(self, n: int):
        self.move_lock = n
        self.last_facing = n

    def modify_ms(self, n: float):
        self.ms_amp = n

    def get_descend(self, delta: float) -> Vector2:
        return self.gravity * delta

    def get_move(self, delta: float, action_state: ActionState) -> Vector2:
        move = Vector2(0, 0)
        speed = self.ms * self.ms_amp

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

        return move * speed * delta