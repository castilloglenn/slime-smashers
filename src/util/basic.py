from absl import flags

FLAGS = flags.FLAGS


def append_list(orig: set, to_add: list):
    for a in to_add:
        orig.add(a)


def remove_list(orig: set, to_del: list):
    for r in to_del:
        if r in orig:
            orig.remove(r)
