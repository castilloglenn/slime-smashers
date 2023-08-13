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
from src.util.logger import TextLogger
from src.util.state import ActionState

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
        title = f"Test Environment | {fnow}"
        pygame.display.set_caption(title)

        total_fps = FLAGS.game.clock.fps
        delta_counter = 0
        fps_counter = 0
        previous_fps = 0

        delta = 0
        joysticks = {}
        p2_joy_id = None

        """TEXT LOGGER"""
        text_logger = TextLogger(
            size=16, rel_x=0.02, rel_y=0.615, rel_nline=0.03, rel_col=0.192
        )
        ActionState.preload(text_logger=text_logger)
        Player.preload(text_logger=text_logger)
        Platform.preload(text_logger=text_logger)

        """GAME OBJECTS"""
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

        """GAME LOOP"""
        while self.running:
            delta = self.clock.tick(FLAGS.game.clock.fps) / 1000
            if delta > FLAGS.game.clock.max_delta:
                print(f"delta overriden: {delta} second(s)")
                delta = FLAGS.game.clock.max_delta

            delta_counter += delta
            fps_counter += 1
            if delta_counter >= 1:
                delta_counter -= 1
                previous_fps = fps_counter
                fps_counter = 0
            f"  FPS: {previous_fps}/{total_fps}"

            """EVENT PROCESSING"""
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

                controller_actions.text_log(text_logger=text_logger)
                text_logger.add_empty()

            keyboard_actions = map_keyboard_action()
            player_2.receive_actions(actions=keyboard_actions)

            player_1.update(delta=delta, collisions=p1_collisions)
            player_2.update(delta=delta, collisions=p2_collisions)

            keyboard_actions.text_log(text_logger=text_logger)

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
