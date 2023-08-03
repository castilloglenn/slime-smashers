from dataclasses import dataclass
from typing import *

from absl import flags
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
from src.util.types import Attribute, Milliseconds

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

    def __post_init__(self):
        self.strike_ms = self.strike_ms / 1000
        self.total_ms = self.total_ms / 1000
        self.debug_ms = 1000

        self.status = AttackSequence.DISABLED
        self.missed = get_surface(rect=self.hitbox, color=(255, 0, 0, 128))
        self.hit = get_surface(rect=self.hitbox, color=(255, 255, 0, 128))

    @property
    def is_attacking(self) -> bool:
        return self.status != AttackSequence.DISABLED

    @property
    def rect(self) -> Rect:
        if self.is_facing_right:
            return get_hitbox_from_rect(rect=self.player_rect, hitbox=self.hitbox)
        else:
            return get_reversed_hitbox_from_rect(
                rect=self.player_rect, hitbox=self.hitbox
            )

    def start(self):
        self.status = AttackSequence.WINDUP
        self.time = 0.0
        self.has_struck = False

    def update(
        self,
        delta: float,
        collisions: list[Sprite],
        player_rect: Rect,
        is_facing_right: bool,
    ):
        self.time += delta
        self.player_rect = player_rect

        if not self.has_struck:
            if self.time >= self.strike_ms:
                self.status = AttackSequence.STRIKE
                self.has_struck = True
                self.is_facing_right = is_facing_right

                self.strike_status = self.missed
                if collision := get_collided(rect=self.rect, collisions=collisions):
                    if Attribute.Health in collision.attributes:
                        self.strike_status = self.hit

        elif self.time < self.total_ms:
            self.status = AttackSequence.RECOVERY
        else:
            self.status = AttackSequence.DISABLED

    def cancel(self):
        self.status = AttackSequence.DISABLED

    def draw(self, surface: Surface):
        if not FLAGS.game.debug.attacks:
            return None

        if self.status != AttackSequence.STRIKE:
            return None

        # TODO Happens so fast, must stay for a while
        surface.blit(self.strike_status, self.rect.topleft)
