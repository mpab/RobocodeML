import copy
import cfg


class Features(object):
    pass


def scale(features):
    mod = copy.copy(features)
    mod.x = (mod.x // 10) / 80
    mod.y = (mod.y // 10) / 60
    mod.enemy_x = (mod.enemy_x // 10) / 80
    mod.enemy_y = (mod.enemy_y // 10) / 60
    mod.heading = (mod.heading // 45) / 8
    mod.enemy_bearing = (mod.enemy_bearing // 45) / 8
    mod.enemy_distance = (mod.enemy_distance // 100) / 10
    return mod


def binarise(features):
    mod = copy.copy(features)
    mod.enemy_collisions = mod.enemy_collisions and 1
    mod.wall_collisions = mod.wall_collisions and 1
    mod.shell_hits = mod.shell_hits and 1
    mod.shell_wounds = mod.shell_wounds and 1
    mod.shell_intercepts = mod.shell_intercepts and 1
    return mod


def classify(features):
    mod = copy.copy(features)
    mod.enemy_collisions = "C" + str(mod.enemy_collisions)
    mod.wall_collisions = "C" + str(mod.wall_collisions)
    mod.shell_hits = "C" + str(mod.shell_hits)
    mod.shell_wounds = "C" + str(mod.shell_wounds)
    mod.shell_intercepts = "C" + str(mod.shell_intercepts)
    return mod


def observation_to_features(obs):

    feat = None

    if obs.scanned:  # filter out invalid features
        feat = Features()
        feat.action = obs.action
        feat.x = obs.x
        feat.y = obs.y
        feat.heading = obs.heading
        feat.enemy_distance = obs.scanned_enemy_distance
        feat.enemy_bearing = obs.scanned_enemy_bearing
        feat.enemy_x = obs.scanned_enemy_x
        feat.enemy_y = obs.scanned_enemy_y
        feat.enemy_collisions = obs.enemy_collisions
        feat.wall_collisions = obs.wall_collisions
        feat.shell_hits = obs.shell_hits
        feat.shell_wounds = obs.shell_wounds
        feat.shell_intercepts = obs.shell_intercepts

    return feat


def csv_append(filepath, feat):
    record = "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        feat.action,
        feat.x,
        feat.y,
        feat.heading,
        feat.enemy_distance,
        feat.enemy_bearing,
        feat.enemy_x,
        feat.enemy_y,
        feat.enemy_collisions,
        feat.wall_collisions,
        feat.shell_hits,
        feat.shell_wounds,
        feat.shell_intercepts)

    with open(str(filepath), 'a') as handle:
        handle.write("{}\n".format(record))


def csv_create(filepath):
    header = ""
    for col in cfg.csv_column_names:
        header = header + col + ","

    header = header.rstrip(",")

    with open(str(filepath), 'w') as handle:
        handle.write("{}\n".format(header))
