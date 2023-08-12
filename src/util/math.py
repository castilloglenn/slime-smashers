from typing import *

from absl import flags
from pygame import Rect, Vector2
from pygame.sprite import Sprite

from src.util.types import HitboxRelPos

FLAGS = flags.FLAGS


def add_vector_to_rect(rect: Rect, vector: Vector2):
    rect.x += vector.x
    rect.y += vector.y


def place_rect_on_top(top: Rect, bottom: Rect):
    top.y = bottom.y - top.height


def contain_rect_in_window(rect: Rect):
    # Enables sprites to jump over the window for a brief moment
    above_offset = 300
    window_rect = Rect(
        0,
        -above_offset,
        FLAGS.game.window.width,
        FLAGS.game.window.height + above_offset,
    )
    rect.clamp_ip(window_rect)


def get_hitbox_from_rect(rect: Rect, hitbox: HitboxRelPos) -> Rect:
    x = rect.x + int(rect.width * hitbox.x)
    y = rect.y + int(rect.height * hitbox.y)
    width = int(rect.width * hitbox.width)
    height = int(rect.height * hitbox.height)
    return Rect(x, y, width, height)


def get_reversed_hitbox_from_rect(rect: Rect, hitbox: HitboxRelPos) -> Rect:
    regular = get_hitbox_from_rect(rect=rect, hitbox=hitbox)

    x_excess = (regular.x + regular.width) - (rect.x + rect.width)

    x = rect.x - x_excess
    y = regular.y
    width = regular.width
    height = regular.height

    return Rect(x, y, width, height)


def get_rect_offset(inside: Rect, enclosure: Rect) -> Vector2:
    return Vector2(inside.x - enclosure.x, inside.y - enclosure.y)


def get_collided(rect: Rect, collisions: list[Sprite]) -> Sprite:
    for collision in collisions:
        if rect.colliderect(collision.rect):
            return collision
    return None


def get_parabolic_position(time: float, duration: float) -> float:
    return -1 * time**2 + duration * time


def get_parabolic_peak_time(duration: float) -> tuple[float, float]:
    return -duration / -2
