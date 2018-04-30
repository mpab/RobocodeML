import copy
import feature_cfg


class Features(object):
    pass


def xxset_reward(features, reward):
    val = 0
    if reward == 0:
        val = features.enemy_collisions * .2 + \
                          features.wall_collisions * .2 + \
                          features.shell_wounds * .6

    if reward == 1:
        val = features.enemy_collisions * .3 + \
                          features.wall_collisions * .3 + \
                          features.shell_wounds * .4

    if reward == 2:
        val = features.enemy_collisions * .1 + \
                          features.wall_collisions * .2 + \
                          features.shell_wounds * .7

    if reward == 3:
        val = features.enemy_collisions * .2 + \
                          features.wall_collisions * .1 + \
                          features.shell_wounds * .7

    if reward == 4:
        val = features.enemy_collisions * .1 + \
                          features.wall_collisions * .1 + \
                          features.shell_wounds * .8

    features.reward = "R{0:.2f}".format(val)


def scale(features):
    scaled = copy.copy(features)
    scaled.x = (scaled.x // 10) / 80
    scaled.y = (scaled.y // 10) / 60
    scaled.enemy_x = (scaled.enemy_x // 10) / 80
    scaled.enemy_y = (scaled.enemy_y // 10) / 60
    scaled.heading = (scaled.heading // 45) / 8
    scaled.enemy_bearing = (scaled.enemy_bearing // 45) / 8
    scaled.enemy_distance = (scaled.enemy_distance // 100) / 10

    scaled.enemy_collisions = scaled.enemy_collisions and 1
    scaled.wall_collisions = scaled.wall_collisions and 1
    scaled.shell_hits = scaled.shell_hits and 1
    scaled.shell_wounds = scaled.shell_wounds and 1
    scaled.shell_intercepts = scaled.shell_intercepts and 1

    return scaled


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


def csv_append_regression(filepath, feat):
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


def csv_append_classification(filepath, feat):
    record = "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        feat.action,
        feat.x,
        feat.y,
        feat.heading,
        feat.enemy_distance,
        feat.enemy_bearing,
        feat.enemy_x,
        feat.enemy_y,
        "C" + str(feat.enemy_collisions),
        "C" + str(feat.wall_collisions),
        "C" + str(feat.shell_hits),
        "C" + str(feat.shell_wounds),
        "C" + str(feat.shell_intercepts))

    with open(str(filepath), 'a') as handle:
        handle.write("{}\n".format(record))


def csv_create(filepath):
    header = ""
    for col in feature_cfg.csv_column_names:
        header = header + col + ","

    header = header.rstrip(",")

    with open(str(filepath), 'w') as handle:
        handle.write("{}\n".format(header))
