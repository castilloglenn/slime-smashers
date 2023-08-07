from absl import flags
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

FLAGS = flags.FLAGS


def get_font(font_name: str, font_size: int) -> Font:
    return Font(name=FLAGS.game.path.ttf[font_name], size=font_size)


def get_bitmap(
    font: Font, text: str, antialias: bool = True, color: Color = (0, 0, 0)
) -> Surface:
    return font.render(text=text, antialias=antialias, color=color)
