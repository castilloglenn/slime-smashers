from typing import *

from absl import flags
from pygame import SRCALPHA
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

from src.util.types import Coordinate, Pixels

FLAGS = flags.FLAGS


def get_font(name: str, size: int) -> Font:
    return Font(FLAGS.game.path.ttf[name], size)


def get_bitmap(
    font: Font,
    text: str,
    antialias: bool = True,
    color: Color = (255, 255, 255),
    bgcolor: Optional[Color] = None,
) -> Surface:
    text_surface = font.render(text, antialias, color)
    if bgcolor is None:
        return text_surface

    bitmap = Surface(text_surface.get_size(), SRCALPHA)
    bitmap.fill(bgcolor)
    bitmap.blit(text_surface, (0, 0))
    return bitmap


def blit_text_shadowed(
    text: str,
    font: Font,
    coord: Coordinate,
    surface: Surface,
    distance: Pixels = 1,
    color: Color = (255, 255, 255),
    bgcolor: Optional[Color] = None,
):
    white = get_bitmap(font=font, text=text, color=color, bgcolor=bgcolor)
    black = get_bitmap(font=font, text=text, color=(0, 0, 0))

    surface.blit(black, (coord[0] + distance, coord[1] + distance))
    surface.blit(white, coord)
