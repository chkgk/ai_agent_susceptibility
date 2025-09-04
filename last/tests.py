from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        yield B5i, {
            "b5_intellect_1": random.randint(1, 5),
            "b5_intellect_2": random.randint(1, 5),
            "b5_intellect_3": random.randint(1, 5),
            "b5_intellect_4": random.randint(1, 5),
            "b5_intellect_5": random.randint(1, 5),
            "b5_intellect_6": random.randint(1, 5),
            "b5_intellect_7": random.randint(1, 5),
            "b5_intellect_8": random.randint(1, 5),
            "b5_intellect_9": random.randint(1, 5),
            "b5_intellect_10": random.randint(1, 5),
        }
        
        edu_level = random.randint(1, 6)
        edu_major = "Economics" if edu_level > 2 else None
            
        yield Demographics, {
            'age': random.randint(18, 100),
            'gender': random.randint(1, 5),
            'race': random.randint(1, 7),
            'education_level': edu_level,
            'education_major': edu_major,
            'political_view': random.randint(1, 100),
            'income_level': random.randint(1, 9),
            'comment': 'No comment.'
        }
        yield LastPage