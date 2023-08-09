import random
from datetime import datetime

import pygame
from absl import flags
from pygame.sprite import Group

from src.asset import get_assets
from src.cluster.platform import Platform
from src.cluster.player import Player
from src.util.input import (
    add_new_controller,
    map_controller_action,
    map_keyboard_action,
    remove_controller,
)
from src.util.math import debug_delta
from src.util.text import StateToTextLogger

FLAGS = flags.FLAGS


class TestEnvironment:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode(
            size=(FLAGS.game.window.width, FLAGS.game.window.height)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.asset = get_assets()
        pygame.display.set_icon(self.asset["game-icon"])

        try:
            self.start()
        finally:
            pygame.quit()

    def start(self):
        """SETTING"""
        now = datetime.now()
        dt_format = "%B %d, %Y"
        fnow = now.strftime(dt_format)

        total_fps = FLAGS.game.clock.fps
        delta_counter = 0
        fps_counter = 0
        previous_fps = 0

        delta = 0
        joysticks = {}
        p2_joy_id = None

        player_1 = Player(sheet=self.asset["green-slime"], rel_x=0.4)
        player_2 = Player(sheet=self.asset["blue-slime"], rel_x=0.6)
        player_2.animations.hz_flip = True
        player_2.motion.last_facing = player_2.motion.LEFT
        players = Group(player_1, player_2)

        platform_1 = Platform(
            rel_x=0.0, rel_y=0.55, rel_width=1.0, rel_height=0.5, disable_debug=True
        )
        platform_2 = Platform(
            rel_x=0.335, rel_y=0.36, rel_width=0.3282, rel_height=0.063
        )
        platform_3 = Platform(
            rel_x=0.069, rel_y=0.205, rel_width=0.207, rel_height=0.063
        )
        platform_4 = Platform(
            rel_x=0.725, rel_y=0.205, rel_width=0.207, rel_height=0.063
        )
        platforms = Group(platform_1, platform_2, platform_3, platform_4)

        p1_collisions = Group(platforms, player_2)
        p2_collisions = Group(platforms, player_1)

        text_logger = StateToTextLogger(
            font_size=16, rel_x=0.02, rel_y=0.615, rel_nline=0.03
        )

        """GAME LOOP"""
        while self.running:
            title = f"Test Environment | {fnow}"
            pygame.display.set_caption(title)

            delta_counter += delta
            fps_counter += 1
            if delta_counter >= 1:
                delta_counter -= 1
                previous_fps = fps_counter
                fps_counter = 0

            text_logger.add(f"FPS: {previous_fps}/{total_fps}")
            text_logger.add("")

            """EVENT PROCESSING"""
            delta = self.clock.tick(FLAGS.game.clock.fps) / 1000
            if delta > FLAGS.game.clock.max_delta:
                print(debug_delta(delta=delta))
                continue

            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.JOYDEVICEADDED:
                        p2_joy_id = add_new_controller(event=event, joysticks=joysticks)

                    if event.type == pygame.JOYDEVICEREMOVED:
                        remove_controller(event=event, joysticks=joysticks)
            except SystemError as e:
                print(f"{e}\nPossible controller previously connected cannot be found.")

            if joysticks:
                controller_actions = map_controller_action(
                    joysticks=joysticks, joy_id=p2_joy_id
                )
                player_1.receive_actions(actions=controller_actions)
                # text_logger.add("[P1: Joystick]")
                # text_logger.add(controller_actions.text_state)

            keyboard_actions = map_keyboard_action()
            player_2.receive_actions(actions=keyboard_actions)

            player_1.update(delta=delta, collisions=p1_collisions)
            player_2.update(delta=delta, collisions=p2_collisions)

            # text_logger.add("[Sprite Green Slime]")
            # text_logger.add(player_1.text_state)
            # text_logger.add("")

            text_logger.add("[P2 Keyboard]")
            text_logger.add(keyboard_actions.text_state)
            text_logger.add("[Sprite: Blue Slime]")
            text_logger.add(player_2.text_state)

            """DISPLAY PROCESSING"""
            self.screen.blit(source=self.asset["test_env_bg"], dest=(0, 0))

            for player in players:
                player.draw(surface=self.screen)

            if FLAGS.game.debug.bounds:
                for land in platforms:
                    land.show_bounds(surface=self.screen)
                for player in players:
                    player.draw_bounds(surface=self.screen)

            text_logger.draw(surface=self.screen)

            pygame.display.flip()
