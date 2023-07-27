import json

import pygame
from absl import flags
from pygame.locals import RLEACCEL

FLAGS = flags.FLAGS


def load_spritesheet_json(filepath: str) -> tuple[dict, dict]:
    with open(file=filepath, mode="r") as json_file:
        json_dict = json.load(json_file)

    parsed_frames = {}
    frames = json_dict["frames"]
    for idx_frame in range(len(frames)):
        parsed_frames[idx_frame] = frames[str(idx_frame)]["frame"]
        parsed_frames[idx_frame]["duration"] = frames[str(idx_frame)]["duration"]

    parsed_tags = json_dict["meta"]["frameTags"]

    return parsed_frames, parsed_tags


def load_png(filepath: str) -> pygame.Surface:
    image = pygame.image.load(filepath)
    image = image.convert_alpha()
    image.set_colorkey((0, 0, 0), RLEACCEL)

    return image
