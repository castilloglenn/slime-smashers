from dataclasses import dataclass
from typing import *

from pygame.surface import Surface

PixelPerSec = int
Pixels = int
Seconds = float


class SpritesheetData(TypedDict):
    x: int
    y: int
    w: int
    h: int
    duration: int


class SpritesheetFrameData(TypedDict):
    index: SpritesheetData


class SpritesheetTagData(TypedDict):
    name: str
    from_: int
    to: int
    direction: str


@dataclass
class SpritesheetDict:
    image: Surface
    frames: SpritesheetFrameData
    tags: list[SpritesheetTagData]
