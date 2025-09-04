from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
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