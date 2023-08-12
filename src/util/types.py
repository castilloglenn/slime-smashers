from dataclasses import dataclass
from enum import Enum
from typing import *

from pygame.surface import Surface

# Unit of Measurements
PixelPerSec = int
Pixels = int
Seconds = float
Milliseconds = int
Coordinate = (int, int)


class Attribute(Enum):
    Health: int = 0
    Motion: int = 1


class StatusEffect(Enum):
    Invulnerable: int = 0


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


FontSurface = Surface


class PreloadTyped(TypedDict):
    str_value: FontSurface
