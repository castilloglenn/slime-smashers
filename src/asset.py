from absl import flags

from src.util.file_io import load_png, load_spritesheet_json
from src.util.image import upscale_surface
from src.util.types import SpritesheetDict

FLAGS = flags.FLAGS


def get_assets() -> dict:
    asset = {}
    parsed_pngs = []

    for file_type in FLAGS.game.path:
        if file_type == "json":
            for file in FLAGS.game.path[file_type]:
                surface = load_png(filepath=FLAGS.game.path.png[file])
                frames, tags = load_spritesheet_json(
                    filepath=FLAGS.game.path[file_type][file]
                )
                asset[file] = SpritesheetDict(image=surface, frames=frames, tags=tags)
                parsed_pngs.append(file)

        elif file_type == "png":
            for file in FLAGS.game.path[file_type]:
                if file in parsed_pngs:
                    continue

                surface = load_png(filepath=FLAGS.game.path.png[file])
                scaled_surface = upscale_surface(surface=surface)
                asset[file] = scaled_surface

    return asset
