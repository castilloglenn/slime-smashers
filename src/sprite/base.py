from itertools import cycle
from typing import *

from absl import flags
from pygame import SRCALPHA, Vector2, transform
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from src.util.image import upscale_surface
from src.util.types import SpritesheetDict

FLAGS = flags.FLAGS


def get_frame_data_via_tag(spritesheet: SpritesheetDict, tag_name: str) -> dict:
    data = {}

    tag_data = None
    for tag in spritesheet.tags:
        if tag["name"] == tag_name:
            tag_data = tag
            break
    else:
        raise KeyError("Sprite: Invalid tag name")

    for idx_ordered, idx_frame in enumerate(
        range(tag_data["from"], tag_data["to"] + 1)
    ):
        data[idx_ordered] = spritesheet.frames[idx_frame]

    return data


class Animation(Sprite):
    def __init__(
        self,
        spritesheet: SpritesheetDict,
        tag_name: Optional[str] = None,
        loops: int = -1,
    ) -> None:
        super().__init__()
        self.spritesheet = spritesheet.image

        if tag_name is not None:
            self.data = get_frame_data_via_tag(
                spritesheet=spritesheet, tag_name=tag_name
            )
        else:
            self.data = spritesheet.frames

        self.loops = loops  # -1 is infinite

        self.frames = self.parse_frames()
        self.n_frames = len(self.frames)
        self.reset_frames()

        self.frame_duration_count = 0.0
        self.total_frame_iterations = self.n_frames * loops
        self.frame_iterations = 0

        self.rect = self.current_frame.get_rect()

    def reset_frames(self):
        self.frame_idx_cycle = cycle(range(self.n_frames))
        self.frame_idx = next(self.frame_idx_cycle)
        self.frame_iterations = 0

    def parse_frames(self) -> list[tuple[Surface, float]]:
        frames = []
        for idx_frame in self.data:
            frame = self.data[idx_frame]
            w = frame["w"]
            h = frame["h"]

            original_surface = Surface((w, h), SRCALPHA)
            area = Rect(frame["x"], frame["y"], w, h)
            original_surface.blit(source=self.spritesheet, dest=(0, 0), area=area)

            scaled_surface = upscale_surface(surface=original_surface)
            duration = frame["duration"] / 1000
            frames.append((scaled_surface, duration))

        return frames

    def update(self, delta: float) -> bool:
        if self.loops > 0:
            if self.frame_iterations >= self.total_frame_iterations:
                self.reset_frames()
                return False

        if delta > FLAGS.game.clock.max_delta:
            return True

        self.frame_duration_count += delta
        if self.frame_duration_count >= self.current_frame_duration:
            self.frame_duration_count -= self.current_frame_duration
            self.frame_idx = next(self.frame_idx_cycle)
            self.frame_iterations += 1

        return True

    def draw(self, surface: Surface, topleft: Vector2, hz_flip: bool = False):
        frame = self.current_frame
        if hz_flip:
            copy = frame.copy()
            frame = transform.flip(copy, True, False)

        surface.blit(source=frame, dest=topleft)

    def __str__(self) -> str:
        return f"Sprite[Fm{self.frame_idx}/{self.n_frames}|Dr{self.current_frame_duration}]"

    @property
    def current_frame(self) -> Surface:
        return self.frames[self.frame_idx][0]

    @property
    def current_frame_duration(self) -> float:
        return self.frames[self.frame_idx][1]
