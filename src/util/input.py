import pygame
from absl import flags
from pygame.event import Event
from pygame.joystick import Joystick

from src.util.state import ActionState

FLAGS = flags.FLAGS


class Xbox:
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    Back = 6
    Start = 7
    Left_Stick = 8
    Right_Stick = 9
    Xbox = 10

    @staticmethod
    def map_buttondown(action_state: ActionState, joystick: Joystick):
        if joystick.get_button(Xbox.A):
            action_state.attack = 1
        if joystick.get_button(Xbox.B):
            action_state.defend = 1

        if joystick.get_button(Xbox.X):
            action_state.jump = 1
        if joystick.get_button(Xbox.LB) and action_state.is_moving:
            action_state.dash = 1

    @staticmethod
    def map_axismotion(action_state: ActionState, joystick: Joystick):
        axis_0 = round(joystick.get_axis(0), 2)
        if axis_0 < 0:
            action_state.move_left = 1
        elif axis_0 > 0:
            action_state.move_right = 1

        axis_1 = round(joystick.get_axis(1), 2)
        if axis_1 < 0:
            action_state.move_up = 1
        elif axis_1 > 0:
            action_state.move_down = 1

        axis_2 = round(joystick.get_axis(2), 2)
        if axis_2 < 0:  # Right stick left
            ...
        elif axis_2 > 0:  # Right stick right
            ...

        axis_3 = round(joystick.get_axis(3), 2)
        if axis_3 < 0:  # Right stick up
            ...
        elif axis_3 > 0:  # Right stick down
            ...

        axis_4 = round(joystick.get_axis(4), 2)
        if axis_4 == 1:  # ZL button
            action_state.defend = 1

        axis_5 = round(joystick.get_axis(5), 2)
        if axis_5 == 1:  # ZR button
            action_state.attack = 1

    @staticmethod
    def map_hatmotion(action_state: ActionState, joystick: Joystick):
        hat = joystick.get_hat(0)
        if hat[1] > 0:
            action_state.move_up = 1
        if hat[1] < 0:
            action_state.move_down = 1
        if hat[0] < 0:
            action_state.move_left = 1
        if hat[0] > 0:
            action_state.move_right = 1


class SwitchPro:
    A = 0
    B = 1
    X = 2
    Y = 3
    Minus = 4
    Home = 5
    Plus = 6
    Left_Stick = 7
    Right_Stick = 8
    L = 9
    R = 10
    Hat_Up = 11
    Hat_Down = 12
    Hat_Left = 13
    Hat_Right = 14
    Capture = 15

    @staticmethod
    def map_buttondown(action_state: ActionState, joystick: Joystick):
        if joystick.get_button(SwitchPro.B):
            action_state.attack = 1
        if joystick.get_button(SwitchPro.A):
            action_state.defend = 1

        if joystick.get_button(SwitchPro.Y):
            action_state.jump = 1
        if joystick.get_button(SwitchPro.L) and action_state.is_moving:
            action_state.dash = 1

        if joystick.get_button(SwitchPro.Hat_Up):
            action_state.move_up = 1
        if joystick.get_button(SwitchPro.Hat_Down):
            action_state.move_down = 1
        if joystick.get_button(SwitchPro.Hat_Left):
            action_state.move_left = 1
        if joystick.get_button(SwitchPro.Hat_Right):
            action_state.move_right = 1

    @staticmethod
    def map_axismotion(action_state: ActionState, joystick: Joystick):
        tolerance = 0.25

        axis_0 = round(joystick.get_axis(0), 2)
        if axis_0 < -tolerance:
            action_state.move_left = 1
        elif axis_0 > tolerance:
            action_state.move_right = 1

        axis_1 = round(joystick.get_axis(1), 2)
        if axis_1 < -tolerance:
            action_state.move_up = 1
        elif axis_1 > tolerance:
            action_state.move_down = 1

        axis_2 = round(joystick.get_axis(2), 2)
        if axis_2 < -tolerance:  # Right stick left
            ...
        elif axis_2 > tolerance:  # Right stick right
            ...

        axis_3 = round(joystick.get_axis(3), 2)
        if axis_3 < -tolerance:  # Right stick up
            ...
        elif axis_3 > tolerance:  # Right stick down
            ...

        axis_4 = round(joystick.get_axis(4), 2)
        if axis_4 == 1:  # ZL button
            ...

        axis_5 = round(joystick.get_axis(5), 2)
        if axis_5 == 1:  # ZR button
            ...

    @staticmethod
    def map_hatmotion(action_state: ActionState, joystick: Joystick):
        pass


CONTROLLERS = {"Xbox 360 Controller": Xbox, "Nintendo Switch Pro Controller": SwitchPro}


def add_new_controller(event: Event, joysticks: dict[int, Joystick]) -> int:
    joy = pygame.joystick.Joystick(event.device_index)
    jid = joy.get_instance_id()
    joysticks[jid] = joy
    print(f"{joy.get_name()} connected. Assigned ID: {jid}")

    return jid


def remove_controller(event: Event, joysticks: dict[int, Joystick]):
    del joysticks[event.instance_id]
    print(f"Joystick {event.instance_id} disconnected")


def map_controller_action(joysticks: dict[int, Joystick], joy_id: int) -> ActionState:
    action_state = ActionState()
    if not joysticks:
        return action_state

    joystick = joysticks[joy_id]
    name = joystick.get_name()
    controller = CONTROLLERS[name]

    controller.map_axismotion(action_state=action_state, joystick=joystick)
    controller.map_hatmotion(action_state=action_state, joystick=joystick)
    controller.map_buttondown(action_state=action_state, joystick=joystick)

    return action_state


def map_keyboard_action() -> ActionState:
    action_state = ActionState()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        action_state.jump = 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        action_state.move_down = 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        action_state.move_left = 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        action_state.move_right = 1

    if keys[pygame.K_j]:
        action_state.attack = 1
    if keys[pygame.K_k]:
        action_state.defend = 1

    if keys[pygame.K_LSHIFT] and action_state.is_moving:
        action_state.dash = 1
    if keys[pygame.K_SPACE]:
        action_state.jump = 1

    return action_state


def is_new_only(old: ActionState, new: ActionState, attr: str) -> bool:
    return getattr(new, attr) and not getattr(old, attr)


def is_old_only(old: ActionState, new: ActionState, attr: str) -> bool:
    return getattr(old, attr) and not getattr(new, attr)
