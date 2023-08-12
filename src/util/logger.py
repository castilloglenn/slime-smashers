from absl import flags
from pygame import Surface

from src.util.text import get_bitmap, get_font
from src.util.types import Coordinate, FontSurface, PreloadTyped

FLAGS = flags.FLAGS


KEYPAIR_FMT = "{key}: {value}"
INDENT_FMT = "  {value}"


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

        self.max_lines = 12

    def preload(self, value: str, indented: bool = False):
        if value in self.preloaded:
            return None

        if indented:
            text = INDENT_FMT.format(value=value)
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

        if value is not None:
            font_surface = self.preloaded[value]
            self.to_display.append(((x, y), font_surface))
        else:
            self.to_display.append(((x, y), None))

    def decide(
        self,
        category: str,
        values: list[str],
        conditions: list[bool],
        default: str = "",
    ):
        value = default
        for c, v in zip(conditions, values):
            if c:
                value = v
                break

        self.add(KEYPAIR_FMT.format(key=category, value=value))

    def add_empty(self, num=1):
        for _ in range(num):
            self.add(None)

    def draw(self, surface: Surface):
        for coord, font_surface in self.to_display:
            if font_surface is None:
                continue

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
