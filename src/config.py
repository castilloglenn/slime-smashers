from pathlib import Path

from ml_collections import ConfigDict


def get_assets_paths(directory_path: Path, config: ConfigDict) -> ConfigDict:
    path = Path(directory_path)

    for item in path.iterdir():
        if item.is_file():
            name = item.stem
            extension = item.suffix[1:]

            if extension not in config:
                config[extension] = ConfigDict()

            config[extension][name] = str(item)

        elif item.is_dir():
            get_assets_paths(directory_path=item, config=config)

    return config


def get_paths(dir_name: str) -> ConfigDict:
    path = ConfigDict()

    current_directory = Path(__file__).resolve().parent.parent
    assets_path = current_directory / dir_name
    get_assets_paths(directory_path=assets_path, config=path)

    return path


def get_config() -> ConfigDict:
    c = ConfigDict()
    c.debug = ConfigDict()
    c.path = ConfigDict()
    c.window = ConfigDict()
    c.clock = ConfigDict()
    c.images = ConfigDict()

    # Debug
    c.debug.bounds = False
    c.debug.attacks = True

    # Paths
    c.path = get_paths(dir_name="asset")

    # Window
    c.window.width = 1280
    c.window.height = 720

    # Clock
    c.clock.fps = 60
    c.clock.single_frame = 1 / c.clock.fps
    c.clock.tolerance = 1.1
    c.clock.max_delta = c.clock.single_frame * c.clock.tolerance

    # Images
    c.images.upscale = 4.0

    return c
