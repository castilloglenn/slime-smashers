from absl import flags
from pygame import transform
from pygame.color import Color
from pygame.locals import RLEACCEL, SRCALPHA
from pygame.rect import Rect
from pygame.surface import Surface

FLAGS = flags.FLAGS


def upscale_surface(surface: Surface) -> Surface:
    original_size = surface.get_size()
    new_size = (
        int(original_size[0] * FLAGS.game.images.upscale),
        int(original_size[1] * FLAGS.game.images.upscale),
    )
    scaled_surface = transform.scale(surface, new_size)
    return scaled_surface


def get_surface(rect: Rect, color: Color) -> Surface:
    surface = Surface((rect.width, rect.height), flags=SRCALPHA)
    surface.fill(color)
    surface.set_colorkey((0, 0, 0), RLEACCEL)
    return surface
