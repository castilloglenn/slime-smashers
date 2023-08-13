from dataclasses import dataclass
from typing import *

from absl import flags
from pygame import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

from src.util.logger import TextLogger
from src.util.math import add_vector_to_rect, contain_rect_in_window, get_collided
from src.util.types import Pixels, StatusEffect

FLAGS = flags.FLAGS


@dataclass
class DashSequence:
    speed: Pixels
    distance: Pixels
    travelled: Pixels = 0.0

    DISABLE: int = 0
    ENABLE: int = 1

    LEFT: int = 0
    RIGHT: int = 1

    def __post_init__(self):
        self.right_speed = Vector2(self.speed, 0)
        self.left_speed = Vector2(-self.speed, 0)

        self.status = DashSequence.DISABLE
        self.direction = None

    @staticmethod
    def preload(text_logger: TextLogger):
        text_logger.preload("Dash")
        text_logger.preload("Speed: NORMAL", indented=True)
        text_logger.preload("Distance: NORMAL", indented=True)

        categories = {
            "Direction": ["LEFT", "RIGHT"],
        }
        text_logger.preload_dict(categories=categories)

    @property
    def is_dashing(self) -> bool:
        return self.status == DashSequence.ENABLE

    @property
    def peaked_distance(self) -> bool:
        return self.travelled > self.distance

    @property
    def status_effects(self) -> list[StatusEffect]:
        return [StatusEffect.Invulnerable]

    def text_log(self, text_logger: TextLogger):
        text_logger.add("Dash")
        text_logger.add("Speed: NORMAL")
        text_logger.add("Distance: NORMAL")

        text_logger.decide(
            category="Direction",
            values=["LEFT", "RIGHT"],
            conditions=[
                self.direction == DashSequence.LEFT,
                self.direction == DashSequence.RIGHT,
            ],
        )

    def start(self):
        self.status = DashSequence.ENABLE

    def update(self, player_rect: Rect, delta: float, collisions: list[Sprite]):
        if self.direction == DashSequence.LEFT:
            speed = self.left_speed
        elif self.direction == DashSequence.RIGHT:
            speed = self.right_speed

        new_rect = player_rect.copy()
        displacement = speed * delta
        add_vector_to_rect(rect=new_rect, vector=displacement)
        contain_rect_in_window(rect=new_rect)

        if get_collided(rect=new_rect, collisions=collisions) is not None:
            self.cancel()
        else:
            player_rect.topleft = new_rect.topleft
            self.travelled += displacement.length()
            if self.peaked_distance:
                self.cancel()

    def cancel(self):
        self.travelled = 0.0
        self.status = DashSequence.DISABLE
        self.direction = None
