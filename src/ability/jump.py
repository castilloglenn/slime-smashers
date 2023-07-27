from dataclasses import dataclass
from typing import *

from absl import flags
from pygame.rect import Rect
from pygame.sprite import Sprite

from src.sprite.motion import Pixels, Seconds
from src.util.math import (
    contain_rect_in_window,
    get_collided,
    get_parabolic_peak,
    get_parabolic_position,
)

FLAGS = flags.FLAGS


@dataclass
class JumpSequence:
    duration: Seconds
    length: Pixels
    steepness: float = 1.0

    DISABLE: int = 0
    RISING: int = 1
    FALLING: int = 2

    def __post_init__(self):
        self.status = self.DISABLE
        self.peak_time, self.rel_peak_position = get_parabolic_peak(
            duration=self.duration,
            steepness=self.steepness,
        )

    @property
    def is_jumping(self) -> bool:
        return self.status != JumpSequence.DISABLE

    def start(self, player_rect: Rect):
        self.status = JumpSequence.RISING
        self.start_height = player_rect.y
        self.time = 0.0

    def update(self, player_rect: Rect, delta: float, collisions: list[Sprite]):
        self.time += delta
        new_rect = player_rect.copy()
        rel_position = get_parabolic_position(
            time=self.time,
            duration=self.duration,
            steepness=self.steepness,
        )
        rel_length = round(rel_position / self.rel_peak_position, 3)
        new_height = self.start_height - (self.length * rel_length)
        new_rect.y = new_height
        contain_rect_in_window(rect=new_rect)

        if self.time < self.peak_time:
            self.status = JumpSequence.RISING
        elif self.time > self.peak_time:
            self.status = JumpSequence.FALLING

        if get_collided(rect=new_rect, collisions=collisions) is not None:
            self.cancel()
        else:
            player_rect.y = new_rect.y

        if self.time > self.duration:
            self.status = JumpSequence.DISABLE

    def cancel(self):
        if self.status == JumpSequence.RISING:
            self.status = JumpSequence.FALLING
            self.time = self.peak_time + (self.peak_time - self.time)
        elif self.status == JumpSequence.FALLING:
            self.status = JumpSequence.DISABLE
            self.time = self.duration
