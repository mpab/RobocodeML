import dataset_observation


class Observation(object):
    pass


def json_to_observation(jsn):

    obs = Observation()

    # metadata
    obs.round = jsn['round']
    obs.num_rounds = jsn['num_rounds']
    obs.frame = jsn['frame']
    # features
    obs.action = jsn['action']
    obs.x = jsn['x']
    obs.y = jsn['y']
    obs.heading = jsn['heading']
    obs.scanned = jsn['scanned']
    obs.scanned_enemy_distance = jsn['scanned_enemy_distance']
    obs.scanned_enemy_bearing = jsn['scanned_enemy_bearing']
    # events
    obs.enemy_collisions = jsn['enemy_collisions']
    obs.wall_collisions = jsn['wall_collisions']
    obs.shell_hits = jsn['shell_hits']
    obs.shell_wounds = jsn['shell_wounds']
    obs.shell_misses = jsn['shell_misses']
    obs.shell_intercepts = jsn['shell_intercepts']

    return obs


def csv_append(filepath, obs):
    record = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        obs.round,
        obs.num_rounds,
        obs.frame,
        obs.action,
        obs.x,
        obs.y,
        obs.heading,
        obs.scanned,
        obs.scanned_enemy_distance,
        obs.scanned_enemy_bearing,
        obs.enemy_collisions,
        obs.wall_collisions,
        obs.shell_hits,
        obs.shell_wounds,
        obs.shell_misses,
        obs.shell_intercepts)

    with open(str(filepath), 'a') as handle:
        handle.write("{}\n".format(record))


def csv_create(filepath):
    header = ""
    for col in dataset_observation.csv_column_names:
        header = header + col + ","

    header = header.rstrip(",")

    with open(str(filepath), 'w') as handle:
        handle.write("{}\n".format(header))
