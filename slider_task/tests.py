from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        yield RealEffort, {
            'pos_1': random.randint(1, 100),
            'pos_2': random.randint(1, 100),
            'pos_3': random.randint(1, 100),
            'pos_4': random.randint(1, 100),
            'pos_5': random.randint(1, 100),
        }