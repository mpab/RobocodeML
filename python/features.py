import copy
import dataset


class Features(object):
    pass


def set_reward(features, reward):
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


def normalise_features(features):
    norm = copy.copy(features)
    norm.x = (norm.x // 10) / 80
    norm.y = (norm.y // 10) / 60
    norm.heading = (norm.heading // 45) / 8
    norm.enemy_bearing = (norm.enemy_bearing // 45) / 8
    norm.enemy_distance = (norm.enemy_distance // 100) / 10

    return norm


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
        feat.enemy_collisions = obs.enemy_collisions
        feat.wall_collisions = obs.wall_collisions
        feat.shell_hits = obs.shell_hits
        feat.shell_wounds = obs.shell_wounds
        feat.shell_intercepts = obs.shell_intercepts

    return feat


def csv_append(filepath, feat):
    record = "{},{},{},{},{},{},{}".format(
        feat.action,
        feat.x,
        feat.y,
        feat.heading,
        feat.enemy_distance,
        feat.enemy_bearing,
        feat.reward)

    with open(str(filepath), 'a') as handle:
        handle.write("{}\n".format(record))


def csv_create(filepath):
    header = ""
    for col in dataset.csv_column_names:
        header = header + col + ","

    header = header.rstrip(",")

    with open(str(filepath), 'w') as handle:
        handle.write("{}\n".format(header))
