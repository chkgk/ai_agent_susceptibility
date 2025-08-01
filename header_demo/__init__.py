from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'header_demo'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    def get_context_data(self, **context):
        ctx = super().get_context_data(**context)
        ctx['headers'] = dict(self.request.headers)
        return ctx


class Results(Page):
    pass


page_sequence = [MyPage, Results]
