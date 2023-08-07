from absl import flags
from pygame.color import Color
from pygame.font import Font
from pygame.surface import Surface

FLAGS = flags.FLAGS


def get_font(name: str, size: int) -> Font:
    return Font(FLAGS.game.path.ttf[name], size)


def get_bitmap(
    font: Font, text: str, antialias: bool = True, color: Color = (0, 0, 0)
) -> Surface:
    return font.render(text, antialias, color)
