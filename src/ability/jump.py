from dataclasses import dataclass
from typing import *

from absl import flags
from pygame.rect import Rect
from pygame.sprite import Sprite

from src.ability.motion import Motion
from src.util.input import is_new_only
from src.util.logger import TextLogger
from src.util.math import (
    contain_rect_in_window,
    get_collided,
    get_parabolic_peak_time,
    get_parabolic_position,
)
from src.util.state import ActionState
from src.util.types import Pixels, Seconds

FLAGS = flags.FLAGS


@dataclass
class JumpSequence:
    duration: Seconds
    length: Pixels

    DISABLE: int = 0
    RISING: int = 1
    FALLING: int = 2

    def __post_init__(self):
        self.status = JumpSequence.DISABLE
        self.peak_time = get_parabolic_peak_time(duration=self.duration)
        self.rel_peak_position = get_parabolic_position(
            time=self.peak_time, duration=self.duration
        )

    @staticmethod
    def preload(text_logger: TextLogger):
        text_logger.preload("Jump")
        text_logger.preload("Duration: NORMAL", indented=True)
        text_logger.preload("Length: NORMAL", indented=True)

        categories = {
            "Status": ["DISABLED", "RISING", "FALLING"],
        }
        text_logger.preload_dict(categories=categories)

    @property
    def is_jumping(self) -> bool:
        return self.status != JumpSequence.DISABLE

    def text_log(self, text_logger: TextLogger):
        text_logger.add("Jump")
        text_logger.add("Duration: NORMAL")
        text_logger.add("Length: NORMAL")

        text_logger.decide(
            category="Status",
            values=["DISABLED", "RISING", "FALLING"],
            conditions=[
                self.status == JumpSequence.DISABLE,
                self.status == JumpSequence.RISING,
                self.status == JumpSequence.FALLING,
            ],
        )

        text_logger.add_empty()

    def receive_actions(
        self, old: ActionState, new: ActionState, motion: Motion, rect: Rect
    ) -> bool:
        if not motion.on_ground or self.is_jumping:
            return False

        if is_new_only(old=old, new=new, attr="jump_up"):
            self.start(player_rect=rect)
            motion.on_ground = False
        elif is_new_only(old=old, new=new, attr="jump_down"):
            ...

        return True

    def start(self, player_rect: Rect):
        self.status = JumpSequence.RISING
        self.start_height = player_rect.y
        self.time = 0.0

    def update(self, player_rect: Rect, delta: float, collisions: list[Sprite]):
        self.time += delta

        rel_position = get_parabolic_position(time=self.time, duration=self.duration)
        rel_length = round(rel_position / self.rel_peak_position, 3)
        new_height = self.start_height - (self.length * rel_length)

        new_rect = player_rect.copy()
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
