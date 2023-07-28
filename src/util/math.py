from typing import *

from absl import flags
from pygame import Rect, Vector2
from pygame.sprite import Sprite

FLAGS = flags.FLAGS


def debug_delta(delta: float) -> str:
    delta_ms = delta * 1000
    sf = FLAGS.game.clock.single_frame * 1000
    max_ms = FLAGS.game.clock.max_delta * 1000
    tol = (FLAGS.game.clock.tolerance - 1) * 100

    report = "delta+: "
    report += f"{delta_ms:4,.0f}/{max_ms:2,.0f}ms "
    report += f"[sf: {sf:2,.0f}ms] [tol: {tol:2,.0f}%]"

    return report


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


def get_hitbox_from_rect(rect: Rect, rx: int, ry: int, rw: int, rh: int) -> Rect:
    x = rect.x + int(rect.width * rx)
    y = rect.y + int(rect.height * ry)
    width = int(rect.width * rw)
    height = int(rect.height * rh)
    return Rect(x, y, width, height)


def get_rect_offset(inside: Rect, enclosure: Rect) -> Vector2:
    return Vector2(inside.x - enclosure.x, inside.y - enclosure.y)


def get_collided(rect: Rect, collisions: list[Sprite]) -> Sprite:
    for collision in collisions:
        if rect.colliderect(collision.rect):
            return collision
    return None


def get_parabolic_position(time: float, duration: float, steepness: float) -> float:
    a = -1 * steepness
    b = duration * steepness
    c = 0

    current = a * time**2 + b * time + c

    return current


def get_parabolic_peak(duration: float, steepness: float) -> tuple[float, float]:
    a = -1 * steepness
    b = duration * steepness
    c = 0

    peak_time = -b / (2 * a)
    peak_height = a * peak_time**2 + b * peak_time + c

    return peak_time, peak_height
