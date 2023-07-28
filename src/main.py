import pygame
from absl import flags

from src.asset import get_assets

FLAGS = flags.FLAGS


class Main:
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
        ...
