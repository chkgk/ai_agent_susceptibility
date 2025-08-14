from otree.api import *

doc = """
Your app description
"""




class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent_given = models.BooleanField(initial=False, label="I am 18 years or older, have read the above information and I consent to participate in this study", widget=widgets.CheckboxInput)

# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent_given']
    
class Survey(Page):
    pass


class Result(Page):
    pass


page_sequence = [Consent, Survey, Result]
