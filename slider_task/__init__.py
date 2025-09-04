from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'slider_task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pos_1 = models.IntegerField(min=0, max=100)
    pos_2 = models.IntegerField(min=0, max=100)
    pos_3 = models.IntegerField(min=0, max=100)
    pos_4 = models.IntegerField(min=0, max=100)
    pos_5 = models.IntegerField(min=0, max=100)
    
    sliders_in_middle = models.IntegerField()

# FUNCTIONS
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        for i in range(1, 6):
            setattr(player, f"pos_{i}", random.choice((random.randint(5, 46), random.randint(55, 96))))

# PAGES
class RealEffort(Page):
    form_model = 'player'
    form_fields = ['pos_1', 'pos_2', 'pos_3', 'pos_4', 'pos_5']

    def before_next_page(player, timeout_happened):
        player.sliders_in_middle = sum(1 for pos in [player.pos_1, player.pos_2, player.pos_3, player.pos_4, player.pos_5] if pos == 50)

page_sequence = [RealEffort]
