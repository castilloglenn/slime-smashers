from typing import *

from absl import flags
from pygame import SRCALPHA
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

from src.util.state import ActionState
from src.util.types import Coordinate, FontSurface, Pixels, PreloadTyped

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


class TextLogger:
    def __init__(
        self, size: int, rel_x: float, rel_y: float, rel_nline: float, rel_col: float
    ):
        font_name = "JetBrainsMono-Bold"

        self.font = get_font(name=font_name, size=size)
        self.x = FLAGS.game.window.width * rel_x
        self.y = FLAGS.game.window.height * rel_y
        self.nline = FLAGS.game.window.height * rel_nline
        self.col_size = FLAGS.game.window.width * rel_col

        self.preloaded: PreloadTyped = {}
        self.to_display: list[tuple(Coordinate, FontSurface)] = []

        self.value_format = "  {value}"
        self.max_lines = 12

    def preload(self, value: str, indented: bool = False):
        if value in self.preloaded:
            return None

        if indented:
            text = self.value_format.format(value=value)
            font_surface = get_bitmap(font=self.font, text=text)
        else:
            font_surface = get_bitmap(font=self.font, text=value)

        self.preloaded[value] = font_surface

    def add(self, value: str):
        index = len(self.to_display)
        row = index % self.max_lines
        col = index // self.max_lines

        x_offset = self.col_size * col
        x = self.x + x_offset
        y = self.y + (self.nline * row)

        font_surface = self.preloaded[value]
        self.to_display.append(((x, y), font_surface))

    def draw(self, surface: Surface):
        for coord, font_surface in self.to_display:
            surface.blit(source=font_surface, dest=coord)

        self.to_display = []


# """Basic White Font"""
# font_surface = get_bitmap(
#     font=font, text="Starting point", bgcolor=(0, 0, 0, 32)
# )
# self.screen.blit(font_surface, (fsw, 20))
# """or shadowed"""
# blit_text_shadowed(
#     text=,
#     font=font,
#     coord=(fsw, 50),
#     surface=self.screen,
#     bgcolor=(0, 0, 0, 32),
# )
