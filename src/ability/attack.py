from dataclasses import dataclass
from typing import *

from absl import flags
from pygame.color import Color
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from src.sprite.bound import HitboxRelPos
from src.util.image import get_surface
from src.util.math import (
    get_collided,
    get_hitbox_from_rect,
    get_reversed_hitbox_from_rect,
)
from src.util.types import Attribute, Milliseconds, Seconds

FLAGS = flags.FLAGS


@dataclass
class AttackSequence:
    strike_ms: Milliseconds
    total_ms: Milliseconds
    hitbox: HitboxRelPos

    DISABLED: int = 0
    WINDUP: int = 1
    STRIKE: int = 2
    RECOVERY: int = 3

    MISSED: int = 0
    HIT: int = 1

    def __post_init__(self):
        self.strike_ms = self.strike_ms / 1_000
        self.total_ms = self.total_ms / 1_000

        self.debug_duration: Seconds = 0.1
        self.debug_counter: Seconds = 0.0

        self.status = AttackSequence.DISABLED
        self.strike_status = None

    @property
    def is_attacking(self) -> bool:
        return self.status != AttackSequence.DISABLED

    @property
    def rect(self) -> Rect:
        if self.right_turn:
            return get_hitbox_from_rect(rect=self.player_rect, hitbox=self.hitbox)
        else:
            return get_reversed_hitbox_from_rect(
                rect=self.player_rect, hitbox=self.hitbox
            )

    @property
    def color(self) -> Color:
        if self.strike_status == AttackSequence.MISSED:
            return Color(255, 255, 255, 128)
        elif self.strike_status == AttackSequence.HIT:
            return Color(255, 0, 0, 128)

    def start(self):
        self.status = AttackSequence.WINDUP
        self.time = 0.0
        self.has_struck = False

    def update_requirements(self, player_rect: Rect, right_turn: bool):
        self.player_rect = player_rect
        self.right_turn = right_turn

    def update(self, delta: float, collisions: list[Sprite]):
        self.time += delta
        if not self.has_struck and self.time >= self.strike_ms:
            self.has_struck = True
            self.status = AttackSequence.STRIKE
            if collision := get_collided(rect=self.rect, collisions=collisions):
                if Attribute.Health in collision.attributes:
                    self.strike_status = AttackSequence.HIT
                    return None
            self.strike_status = AttackSequence.MISSED

        elif self.time < self.total_ms:
            self.status = AttackSequence.RECOVERY
        else:
            self.status = AttackSequence.DISABLED

    def cancel(self):
        self.status = AttackSequence.DISABLED

    def draw(self, surface: Surface):
        if not FLAGS.game.debug.attacks:
            return None

        if self.strike_status is None:
            return None

        color_surface = get_surface(rect=self.rect, color=self.color)
        surface.blit(color_surface, self.rect.topleft)

    def debug_update(self, delta: float):
        if not FLAGS.game.debug.attacks:
            return None

        if self.strike_status is None:
            return None

        self.debug_counter += delta
        if self.debug_counter >= self.debug_duration:
            self.strike_status = None
            self.debug_counter = 0.0
