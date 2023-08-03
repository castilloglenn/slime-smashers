from dataclasses import dataclass
from typing import *

from absl import flags
from pygame.rect import Rect
from pygame.sprite import Sprite

from src.sprite.bound import HitboxRelPos
from src.util.types import HasHealth, Milliseconds

FLAGS = flags.FLAGS


@dataclass
class AttackSequence:
    strike_ms: Milliseconds
    hitbox: HitboxRelPos

    DISABLED: int = 0
    WINDUP: int = 1
    STRIKE: int = 2
    RECOVERY: int = 3

    LEFT: int = 0
    RIGHT: int = 1

    def __post_init__(self):
        self.status = AttackSequence.DISABLED

    @property
    def is_attacking(self) -> bool:
        return self.status != AttackSequence.DISABLE

    def start(self, is_facing_right: bool):
        self.status = AttackSequence.WINDUP
        self.facing = int(is_facing_right)
        self.time = 0.0

    def update(self, player_rect: Rect, delta: float, collisions: list[Sprite]):
        self.time += delta

    def cancel(self):
        ...

    def debug(self):
        ...
