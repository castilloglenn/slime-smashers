from typing import *

from absl import flags
from pygame import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from src.ability.attack import AttackSequence
from src.ability.dash import DashSequence
from src.ability.jump import JumpSequence
from src.ability.motion import Motion
from src.sprite.bound import Bound, HitboxRelPos, WindowRelPos
from src.sprite.sheet import Spritesheet
from src.util.basic import append_list, remove_list
from src.util.input import is_new_only, is_old_only
from src.util.math import (
    add_vector_to_rect,
    contain_rect_in_window,
    get_collided,
    place_rect_on_top,
)
from src.util.state import ActionState
from src.util.types import Attribute, SpritesheetDict, StatusEffect

FLAGS = flags.FLAGS


class Player(Sprite):
    def __init__(self, sheet: SpritesheetDict, rel_x: float) -> None:
        super().__init__()

        self.attributes = {Attribute.Health, Attribute.Motion}
        self.status_effects = set()

        self.action = ActionState()
        self.animations = Spritesheet(spritesheet=sheet)
        self.bound = Bound(
            hb_source=self.animations.idle_sprite,
            window=WindowRelPos(rel_x, 0.0),
            hitbox=HitboxRelPos(0.44, 0.45, 0.125, 0.22),
        )

        self.motion = Motion(gravity_=800, ms=450)
        self.jump = JumpSequence(duration=0.7, length=200)
        self.dash = DashSequence(speed=1_000, distance=150)

        self.attack = AttackSequence(
            strike_ms=100,
            total_ms=100,
            hb_source=self.animations.idle_sprite,
            hitbox=HitboxRelPos(0.2, 0.7, 0.5, 0.6),
        )

    @property
    def rect(self) -> Rect:
        return self.bound.hitbox

    @rect.setter
    def rect(self, value: Rect):
        assert isinstance(value, Rect)
        self.bound.update_hitbox(new=value)

    def add_status_effects(self, status_effects: list[StatusEffect]):
        append_list(orig=self.status_effects, to_add=status_effects)

    def del_status_effects(self, status_effects: list[StatusEffect]):
        remove_list(orig=self.status_effects, to_del=status_effects)

    def receive_actions(self, actions: ActionState):
        if self.motion.on_ground:
            if is_new_only(old=self.action, new=actions, attr="jump"):
                if not self.jump.is_jumping:
                    self.jump.start(player_rect=self.rect)

        if not self.animations.is_performing:
            if is_new_only(old=self.action, new=actions, attr="attack"):
                # NOTE Attack starting point
                self.animations.update_perf(new="attack")
            elif actions.defend:
                # NOTE Defend starting point
                self.animations.update_perf(new="defend")
                self.motion.modify_ms(n=0.25)

        if is_old_only(old=self.action, new=actions, attr="defend"):
            # NOTE Defend ending point
            self.animations.reset_perf()
            self.motion.modify_ms(n=1.0)

        if is_new_only(old=self.action, new=actions, attr="dash"):
            if not self.dash.is_dashing:
                self.add_status_effects(self.dash.status_effects)
                self.animations.update_perf(new="dash")
                self.dash.start()
                if actions.move_right:
                    self.dash.direction = DashSequence.RIGHT
                    self.motion.modify_move_lock(n=Motion.RIGHT)
                elif actions.move_left:
                    self.dash.direction = DashSequence.LEFT
                    self.motion.modify_move_lock(n=Motion.LEFT)

        self.action = actions

    def apply_movement(self, delta: float, collisions: list[Sprite]):
        if self.action.is_moving:
            self.animations.hz_flip = not self.motion.is_facing_right

            new_rect = self.rect.copy()
            movement = self.motion.get_move(delta=delta, action_state=self.action)
            add_vector_to_rect(rect=new_rect, vector=movement)
            contain_rect_in_window(rect=new_rect)
            if get_collided(rect=new_rect, collisions=collisions) is not None:
                return None

            self.rect = new_rect

    def apply_jump(self, delta: float, collisions: list[Sprite]):
        self.jump.update(player_rect=self.rect, delta=delta, collisions=collisions)
        self.bound.align_rects()

        if not self.animations.is_performing:
            if self.jump.status == JumpSequence.RISING:
                self.animations.update_idle(new="rise")
            elif self.jump.status == JumpSequence.FALLING:
                self.animations.update_idle(new="fall")
            else:
                self.animations.update_idle(new="idle")

    def apply_dash(self, delta: float, collisions: list[Sprite]):
        self.dash.update(player_rect=self.rect, delta=delta, collisions=collisions)
        self.bound.align_rects()

        if not self.dash.is_dashing:
            self.del_status_effects(self.dash.status_effects)
            self.animations.reset_perf()
            self.motion.move_lock = None

    def apply_gravity(self, delta: float, collisions: list[Sprite]):
        descend = self.motion.get_descend(delta=delta)
        add_vector_to_rect(rect=self.rect, vector=descend)

        if collision := get_collided(rect=self.rect, collisions=collisions):
            place_rect_on_top(top=self.rect, bottom=collision.rect)
            self.animations.update_idle(new="idle")
            self.motion.on_ground = True
        else:
            self.animations.update_idle(new="fall")
            self.motion.on_ground = False

        self.bound.align_rects()

    def update(self, delta: float, collisions: list[Sprite]):
        self.apply_movement(delta=delta, collisions=collisions)

        if self.jump.is_jumping:
            if self.dash.is_dashing:
                if self.jump.status != JumpSequence.FALLING:
                    self.jump.cancel()

                self.apply_dash(delta=delta, collisions=collisions)
            else:
                self.apply_jump(delta=delta, collisions=collisions)
        elif self.dash.is_dashing:
            self.apply_dash(delta=delta, collisions=collisions)
        else:
            self.apply_gravity(delta=delta, collisions=collisions)

        self.animations.update(delta=delta)

    def draw(self, surface: Surface):
        sprite = self.animations.get_sprite()
        sprite.draw(
            surface=surface,
            topleft=self.bound.image_start,
            hz_flip=self.animations.hz_flip,
        )
        self.bound.draw(surface=surface)
        self.attack.draw(surface=surface)
