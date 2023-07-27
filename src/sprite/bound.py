from dataclasses import dataclass
from typing import *

from absl import flags
from pygame import Rect
from pygame.surface import Surface

from src.sprite.base import Animation
from src.util.image import get_surface
from src.util.math import get_hitbox_from_rect, get_rect_offset

FLAGS = flags.FLAGS


@dataclass
class WindowRelPos:
    x: float = 0.5
    y: float = 0.5


@dataclass
class HitboxRelPos:
    x: float = 0.0
    y: float = 0.0
    width: float = 1.0
    height: float = 1.0


@dataclass
class Bound:
    source: Animation
    window: WindowRelPos
    hitbox: HitboxRelPos

    def __post_init__(self):
        self.image_rect = Rect(0, 0, self.source.rect.width, self.source.rect.height)
        self.image_rect.center = (
            int(self.window.x * FLAGS.game.window.width),
            int(self.window.y * FLAGS.game.window.height),
        )
        self.hitbox = get_hitbox_from_rect(
            rect=self.image_rect,
            rx=self.hitbox.x,
            ry=self.hitbox.y,
            rw=self.hitbox.width,
            rh=self.hitbox.height,
        )
        self.hitbox_offset = get_rect_offset(
            inside=self.hitbox, enclosure=self.image_rect
        )
        self.debug_hitbox = get_surface(rect=self.hitbox, color=(255, 0, 255, 64))

    @property
    def image_start(self) -> tuple[int, int]:
        return self.image_rect.topleft

    def align_rects(self):
        self.image_rect.x = self.hitbox.x - self.hitbox_offset.x
        self.image_rect.y = self.hitbox.y - self.hitbox_offset.y

    def update_hitbox(self, new: Rect):
        self.hitbox = new
        self.align_rects()

    def draw(self, surface: Surface):
        if not FLAGS.game.debug.bounds:
            return None

        surface.blit(self.debug_hitbox, self.hitbox.topleft)
