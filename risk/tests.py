from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        yield Submission(HL, {
            f"hl_a_{i}": random.choice([True, False]) for i in range(1, 11)
        }, check_html=False)