from dataclasses import dataclass, field
from typing import *

from absl import flags

from src.sprite.base import Animation
from src.util.types import SpritesheetDict

FLAGS = flags.FLAGS


@dataclass
class Spritesheet:
    spritesheet: SpritesheetDict
    single_loops: list[str] = field(default_factory=lambda: ["attack"])

    def __post_init__(self):
        for tag in self.spritesheet.tags:
            name = tag["name"]
            loops = -1
            if name in self.single_loops:
                loops = 1
            sprite = Animation(spritesheet=self.spritesheet, tag_name=name, loops=loops)
            setattr(self, name, sprite)

        self.idle_sprite: Animation = self.idle
        self.perf_sprite: Optional[Animation] = None
        self.hz_flip = False

    @property
    def is_performing(self) -> bool:
        return self.perf_sprite is not None

    def update_idle(self, new: str):
        new_sprite = getattr(self, new)
        if self.idle_sprite != new_sprite:
            self.idle_sprite.reset_frames()
            self.idle_sprite = new_sprite

    def update_perf(self, new: str):
        if self.is_performing:
            self.perf_sprite.reset_frames()

        self.perf_sprite = getattr(self, new)

    def reset_perf(self):
        if self.is_performing:
            self.perf_sprite.reset_frames()

        self.perf_sprite = None

    def update(self, delta: float):
        if self.is_performing:
            is_playing = self.perf_sprite.update(delta=delta)
        else:
            is_playing = self.idle_sprite.update(delta=delta)

        if not is_playing:
            self.idle_sprite = self.idle
            self.reset_perf()

    def get_sprite(self) -> Animation:
        if self.is_performing:
            sprite = self.perf_sprite
        else:
            sprite = self.idle_sprite

        return sprite
