from dataclasses import dataclass
from typing import *

from absl import flags
from pygame import Vector2

from src.util.math import get_normalized_movement
from src.util.state import ActionState

FLAGS = flags.FLAGS


PixelPerSec = int
Pixels = int
Seconds = float

MovementSpeed: PixelPerSec = int


@dataclass
class Motion:
    gravity_: PixelPerSec
    ms: MovementSpeed

    def __post_init__(self):
        self.gravity = Vector2(0, self.gravity_)
        self.ms_amp = 1.0

        self.on_ground = False

    def modify_ms(self, n: float):
        self.ms_amp = n

    def get_descend(self, delta: float) -> Vector2:
        return self.gravity * delta

    def get_move(self, delta: float, action_state: ActionState) -> Vector2:
        return get_normalized_movement(
            action_state=action_state,
            speed=self.ms,
            speed_ampify=self.ms_amp,
            delta=delta,
        )
