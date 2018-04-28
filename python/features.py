class Observation:
    def __init__(self,):

        # actions
        self.action = -1
        self.x = 0
        self.y = 0
        self.heading = 0
        self.enemy_distance = 0
        self.enemy_bearing = 0

        # events
        self.enemy_collisions = 0
        self.wall_collisions = 0
        self.shell_hits = 0
        self.shell_wounds = 0
        self.shell_misses = 0
        self.shell_intercepts = 0


def csv_append(filepath, obs):
    record = "{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
        obs.round,
        obs.frame,
        obs.action,
        obs.x,
        obs.y,
        obs.heading,
        obs.enemy_distance,
        obs.enemy_bearing,
        obs.enemy_collisions,
        obs.wall_collisions,
        obs.shell_hits,
        obs.shell_wounds,
        obs.shell_misses,
        obs.shell_intercepts)

    with open(str(filepath), 'a') as handle:
        handle.write("{}\n".format(record))


def csv_create(filepath):
    header = "ROUND,FRAME,ACTION," \
             "X,Y,HEADING," \
             "ENEMY_DISTANCE,ENEMY_BEARING," \
             "ENEMY_COLLISIONS,WALL_COLLISIONS," \
             "SHELL_HITS,SHELL_WOUNDS,SHELL_MISSES,SHELL_INTERCEPTS"
    with open(str(filepath), 'w') as handle:
        handle.write("{}\n".format(header))


def extract(jsn):

    obs = Observation()

    # meta info
    obs.round = jsn['round']
    obs.num_rounds = jsn['num_rounds']
    obs.frame = jsn['frame']

    # actions
    obs.action = jsn['action']
    obs.x = jsn['x']
    obs.y = jsn['y']
    obs.enemy_distance = jsn['enemy_distance']
    obs.enemy_bearing = jsn['enemy_bearing']

    # events
    obs.enemy_collisions = jsn['enemy_collisions']
    obs.wall_collisions = jsn['wall_collisions']
    obs.shell_hits = jsn['shell_hits']
    obs.shell_wounds = jsn['shell_wounds']
    obs.shell_misses = jsn['shell_misses']
    obs.shell_intercepts = jsn['shell_intercepts']

    return obs
