import random
from dataclasses import dataclass
from typing import *

from absl import flags

from src.util.logger import KEYPAIR_FMT, TextLogger

FLAGS = flags.FLAGS

Player_ = Any


@dataclass
class ActionState:
    source: str

    move_left = 0
    move_right = 0
    jump_up = 0
    jump_down = 0

    aim_left = 0
    aim_right = 0
    aim_up = 0
    aim_down = 0

    dash = 0
    attack = 0
    defend = 0

    @staticmethod
    def preload(text_logger: TextLogger):
        titles = ["Keyboard", "Joystick", "Randomized"]
        for t in titles:
            text_logger.preload(t)

        categories = {
            "Movement": ["LEFT", "RIGHT"],
            "Action": ["ATTACK", "DEFEND"],
            "Special": ["DASH", "JUMP UP", "JUMP DOWN"],
        }
        text_logger.preload_dict(categories=categories)

    @property
    def is_moving(self) -> bool:
        return any([self.move_left, self.move_right])

    @property
    def is_jumping(self) -> bool:
        return any([self.jump_up, self.jump_down])

    def text_log(self, text_logger: TextLogger):
        text_logger.add(self.source)

        text_logger.decide(
            category="Movement",
            values=["LEFT", "RIGHT"],
            conditions=[self.move_left, self.move_right],
        )

        text_logger.decide(
            category="Action",
            values=["ATTACK", "DEFEND"],
            conditions=[self.attack, self.defend],
        )

        text_logger.decide(
            category="Special",
            values=["JUMP UP", "DASH", "JUMP DOWN"],
            conditions=[self.jump_up, self.dash, self.jump_down],
        )


@dataclass
class ActionStateRandomizer:
    LEFT: int = 0
    RIGHT: int = 1
    STAND: int = 2

    def __init__(self):
        self.fps = FLAGS.game.clock.fps

        self.movement_direction = None
        self.movement_duration = None
        self.movement_counter = 0

        self.action_cooldown = 1
        self.action_counter = 0

        self.special_cooldown = 1
        self.special_counter = 0

    def set_random_direction(self, player: Player_, computer: Player_):
        if self.movement_direction is not None:
            return None

        left_bias = right_bias = 0
        if computer.rect.x > player.rect.x:
            left_bias = 1
        elif computer.rect.x < player.rect.x:
            right_bias = 1

        self.movement_direction = random.choices(
            population=[0, 1, 2], weights=[1 + left_bias, 1 + right_bias, 1]
        )[0]

        lower = random.uniform(0.2, 0.5)
        upper = random.uniform(0.6, 2.4)
        duration = random.choices(population=[lower, upper], weights=[10, 1])[0]
        self.movement_duration = duration
        self.movement_counter = 0

    def move(self, actions: ActionState):
        if self.movement_direction is None:
            return None

        self.movement_counter += 1
        if self.movement_direction == ActionStateRandomizer.RIGHT:
            actions.move_right = 1
        elif self.movement_direction == ActionStateRandomizer.LEFT:
            actions.move_left = 1
        elif self.movement_direction == ActionStateRandomizer.STAND:
            pass

        if self.movement_counter / self.fps >= self.movement_duration:
            self.movement_direction = None

    def action(self, actions: ActionState):
        if self.action_counter / self.fps < self.action_cooldown:
            self.action_counter += 1
            return None

        action = random.choices(population=[0, 1], weights=[1, 1])[0]
        if action == 0:
            actions.attack = 1

        self.action_cooldown = random.uniform(0.3, 0.5)
        self.action_counter = 0

    def special(self, actions: ActionState, player: Player_, computer: Player_):
        if self.special_counter / self.fps < self.special_cooldown:
            self.special_counter += 1
            return None

        jump_bias = 0
        if computer.rect.y > player.rect.y:
            jump_bias = 3

        special = random.choices(population=[0, 1, 2], weights=[3 + jump_bias, 2, 1])[0]
        if special == 1:
            actions.jump_up = 1
        elif special == 2:
            actions.dash = 1

            if computer.rect.x > player.rect.x:
                actions.move_left = 1
            else:
                actions.move_right = 1
        elif special == 3:
            actions.jump_down = 1

        self.special_cooldown = random.uniform(0.3, 0.5)
        self.special_counter = 0

    def get_random_actions(self, player: Player_, computer: Player_) -> ActionState:
        new_actions = ActionState(source="Randomized")

        self.set_random_direction(player=player, computer=computer)
        self.move(actions=new_actions)
        self.action(actions=new_actions)
        self.special(actions=new_actions, player=player, computer=computer)

        return new_actions
