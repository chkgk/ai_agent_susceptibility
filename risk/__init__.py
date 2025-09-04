from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'risk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    HL_LOTTERY = {
        "name": "HL1",
        "lottery_a": {
            "probabilities": [0.5, 0.5],
            "prizes": [
                [0.2 for _ in range(0, 10)],
                [4.2 for _ in range(0, 10)]
            ]
        },
        "lottery_b": {
            "probabilities": [1],
            "prizes": [[0.6, 1.0, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2]]
        },
    }

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    hl_a_1 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_2 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_3 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_4 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_5 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_6 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_7 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_8 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_9 = models.BooleanField(widget=widgets.RadioSelect)
    hl_a_10 = models.BooleanField(widget=widgets.RadioSelect)

# FUNCTIONS
def calculate_payoff(player: Player, lottery):
    max_row = len(lottery["lottery_a"]["prizes"][0])
    random_row = random.randint(1, max_row)
    chose_a = getattr(player, f"hl_a_{random_row}")

    pay_left = random.random() < lottery["lottery_a"]["probabilities"][0]
    if not chose_a:
        lottery_outcome = lottery["lottery_b"]["prizes"][0][random_row - 1]

    else:
        if pay_left:
            lottery_outcome = lottery["lottery_a"]["prizes"][0][random_row - 1]
        else:
            lottery_outcome = lottery["lottery_a"]["prizes"][1][random_row - 1]

    player.payoff = lottery_outcome


# PAGES
class HL(Page):
    form_model = 'player'
    form_fields = [f"hl_a_{i}" for i in range(1, 11)]

    def js_vars(player: Player):
        return {
            'lotteries': C.HL_LOTTERY,
        }

    def before_next_page(player: Player, timeout_happened):
        calculate_payoff(player, C.HL_LOTTERY)


page_sequence = [HL]
