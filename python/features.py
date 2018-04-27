import json

class Observation:
    def __init__(self, frame):
        self.frame = frame;

        # actions
        self.action = -1
        self.x = 0
        self.y = 0
        self.distance = 0
        self.bearing = 0

        # events
        self.enemy_collisions = 0
        self.enemy_hits = 0
        self.wounds = 0
        self.wall_collisions = 0
        self.bullet_misses = 0
        self.bullet_intercepts = 0


class Extractor:

    featuresList = []

    def __init__(self):
        self.observation = None
        self.battle = -1;
        self.max_battles = -1;
        self.frame = -1;
        self.collisions = 0
        self.enemy_hits = 0
        self.bullet_misses = 0
        self.bullet_intercepts = 0
        self.wounds = 0

    def extract_action(cls, json, obs):
        t = json['type']

        if t != 'action':
            return

        obs.action = json['action']
        obs.x = json['x'] 
        obs.y = json['y']
        obs.distance = json['distance']
        obs.bearing = json['bearing']

        return obs


    def extract_event(cls, json, obs):
        t = json['type']

        if t != 'event':
            return

        collision = json['collision']
        obs.enemy_collisions = 

    def extract(cls, msg):
        j = json.loads(msg)
        battle = j['battle']

        if battle > self.battle: # new battle
            self.battle = battle
            self.max_battles = j['max_battles']

            observation = Observation(j['frame'])

            if self.observation is None:
                self.observation = observation
            else:
                featuresList.append(observation)
                self.observation = observation

            Extractor.extract_action(j)
            Extractor.extract_event(j)
