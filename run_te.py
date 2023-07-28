from absl import app
from ml_collections import config_flags

from src.config import get_config
from src.test import TestEnvironment


def run(_):
    TestEnvironment()


if __name__ == "__main__":
    config_flags.DEFINE_config_dict("game", get_config())

    app.run(run)
