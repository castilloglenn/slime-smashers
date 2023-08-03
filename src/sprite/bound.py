from dataclasses import dataclass
from typing import *

from absl import flags
from pygame import Rect
from pygame.surface import Surface

from src.sprite.base import Animation
from src.util.image import get_surface
from src.util.math import get_hitbox_from_rect, get_rect_offset
from src.util.types import HitboxRelPos, WindowRelPos

FLAGS = flags.FLAGS


@dataclass
class Bound:
    image_source: Animation
    window: WindowRelPos
    hitbox: HitboxRelPos

    def __post_init__(self):
        self.image_rect = Rect(
            0, 0, self.image_source.rect.width, self.image_source.rect.height
        )
        self.image_rect.center = (
            int(self.window.x * FLAGS.game.window.width),
            int(self.window.y * FLAGS.game.window.height),
        )
        self.hitbox_rect = get_hitbox_from_rect(
            rect=self.image_rect, hitbox=self.hitbox
        )
        self.hitbox_offset = get_rect_offset(
            inside=self.hitbox_rect, enclosure=self.image_rect
        )
        self.debug_surface = get_surface(rect=self.hitbox_rect, color=(255, 0, 255, 64))

    @property
    def image_start(self) -> tuple[int, int]:
        return self.image_rect.topleft

    def align_rects(self):
        self.image_rect.x = self.hitbox_rect.x - self.hitbox_offset.x
        self.image_rect.y = self.hitbox_rect.y - self.hitbox_offset.y

    def update_hitbox(self, new: Rect):
        self.hitbox_rect = new
        self.align_rects()

    def draw(self, surface: Surface):
        if not FLAGS.game.debug.bounds:
            return None

        surface.blit(self.debug_surface, self.hitbox_rect.topleft)
