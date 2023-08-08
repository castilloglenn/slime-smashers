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
from src.util.text import blit_text_shadowed, get_bitmap, get_font

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

        player_1 = Player(sheet=self.asset["green-slime"], rel_x=0.5)
        player_2 = Player(sheet=self.asset["green-slime"], rel_x=0.75)
        players = Group(player_1, player_2)

        platform_1 = Platform(rel_x=0.0, rel_y=0.74, rel_width=1.0, rel_height=0.26)
        platform_2 = Platform(rel_x=0.1, rel_y=0.5, rel_width=0.2, rel_height=0.04)
        platform_3 = Platform(rel_x=0.4, rel_y=0.325, rel_width=0.2, rel_height=0.04)
        platform_4 = Platform(rel_x=0.7, rel_y=0.5, rel_width=0.2, rel_height=0.04)
        platforms = Group(platform_1, platform_2, platform_3, platform_4)

        p1_collisions = Group(platforms, player_2)
        p2_collisions = Group(platforms, player_1)

        """Font testing"""
        font_name = "JetBrainsMono-Bold"
        font = get_font(name=font_name, size=16)
        fsw = int(FLAGS.game.window.width * 0.9125)

        """GAME LOOP"""
        while self.running:
            delta_counter += delta
            fps_counter += 1
            if delta_counter >= 1:
                delta_counter -= 1
                previous_fps = fps_counter
                fps_counter = 0

            title = f"Test Environment | {fnow}"
            pygame.display.set_caption(title)

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

            keyboard_actions = map_keyboard_action()
            player_2.receive_actions(actions=keyboard_actions)

            player_1.update(delta=delta, collisions=p1_collisions)
            player_2.update(delta=delta, collisions=p2_collisions)

            """DISPLAY PROCESSING"""
            self.screen.blit(source=self.asset["test_env_bg"], dest=(0, 0))

            for player in players:
                player.draw(surface=self.screen)

            if FLAGS.game.debug.bounds:
                for land in platforms:
                    land.show_bounds(surface=self.screen)

            """Basic White Font"""
            font_surface = get_bitmap(
                font=font, text=f"{previous_fps}/{total_fps} FPS", bgcolor=(0, 0, 0, 32)
            )
            self.screen.blit(font_surface, (fsw, 20))
            """or shadowed"""
            blit_text_shadowed(
                text=f"{previous_fps}/{total_fps} FPS",
                font=font,
                coord=(fsw, 50),
                surface=self.screen,
                # bgcolor=(0, 0, 0, 32),
            )
            pygame.display.flip()
