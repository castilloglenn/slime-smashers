from typing import *

from absl import flags
from pygame import SRCALPHA
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

from src.util.state import ActionState
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


class StateToTextLogger:
    def __init__(self, font_size: int, rel_x: float, rel_y: float, rel_nline: float):
        font_name = "JetBrainsMono-Bold"
        self.font = get_font(name=font_name, size=font_size)
        self.x = FLAGS.game.window.width * rel_x
        self.y = FLAGS.game.window.height * rel_y
        self.nl = FLAGS.game.window.height * rel_nline

        self.max_rows = 12
        self.row_lengths = [20, 21, 20]
        self.row_length_idx = 1
        self.data = []

    def add(self, data: str | list):
        if isinstance(data, str):
            self.data.append(data)
        elif isinstance(data, list):
            self.data += data

    def organize(self):
        if len(self.data) <= self.max_rows:
            return None

        next_last = min(self.max_rows * 2, len(self.data))
        for next_idx in range(self.max_rows, next_last):
            current_idx = next_idx - self.max_rows
            row_length = sum(self.row_lengths[: self.row_length_idx])
            while len(self.data[current_idx]) < row_length:
                self.data[current_idx] += " "
            self.data[current_idx] += " | "
            self.data[current_idx] += self.data[next_idx]

        self.data = self.data[: self.max_rows] + self.data[next_last:]
        self.row_length_idx += 1
        self.organize()

    def draw(self, surface: Surface):
        self.organize()

        for i_line, sentence in enumerate(self.data):
            btsurf = get_bitmap(font=self.font, text=sentence)
            surface.blit(btsurf, (self.x, self.y + (self.nl * i_line)))

        self.data = []
        self.row_length_idx = 1


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
