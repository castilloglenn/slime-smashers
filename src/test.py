import pygame
from absl import flags
from pygame.sprite import Group

from src.asset import get_assets
from src.cluster.player import Player
from src.cluster.static import HardSurface
from src.util.input import (
    add_new_controller,
    map_controller_action,
    map_keyboard_action,
    remove_controller,
)
from src.util.math import debug_delta

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

        try:
            self.start()
        finally:
            pygame.quit()

    def start(self):
        delta = 0
        joysticks = {}
        p2_joy_id = None

        player_1 = Player(sheet=self.asset["green-slime"], rel_x=0.5)
        player_2 = Player(sheet=self.asset["green-slime"], rel_x=0.75)
        players = Group(player_1, player_2)

        land_1 = HardSurface(rel_x=0.0, rel_y=0.74, rel_width=1.0, rel_height=0.26)
        land_2 = HardSurface(rel_x=0.25, rel_y=0.5, rel_width=0.25, rel_height=0.04)
        lands = Group(land_1, land_2)

        p1_collisions = Group(lands, player_2)
        p2_collisions = Group(lands, player_1)

        while self.running:
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
                player_2.receive_actions(actions=controller_actions)

            keyboard_actions = map_keyboard_action()
            player_1.receive_actions(actions=keyboard_actions)

            player_1.update(delta=delta, collisions=p1_collisions)
            player_2.update(delta=delta, collisions=p2_collisions)

            """DISPLAY PROCESSING"""
            self.screen.blit(source=self.asset["landscape"], dest=(0, 0))

            for player in players:
                player.draw(surface=self.screen)

            if FLAGS.game.debug.bounds:
                land_1.show_bounds(surface=self.screen)
            land_2.show_bounds(surface=self.screen)

            pygame.display.flip()
