


from otree.api import *
from otree import settings
import requests 
import json 

doc = """
Your app description
"""




class C(BaseConstants):
    NAME_IN_URL = 'human_question'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    captcha_token = models.StringField(
        blank=True
    )
    captcha_score = models.FloatField()
    captcha_result = models.BooleanField(label="Are you a human?")
    captcha_server_response = models.LongStringField()

    consent_given = models.BooleanField(initial=False,
                                        label="I am 18 years or older, have read the above information and I consent to participate in this study",
                                        widget=widgets.CheckboxInput)

# PAGES
class Challenge(Page):
    form_model = 'player'
    form_fields = ['consent_given', 'captcha_result']

    def before_next_page(player, timeout_happened):
        player.captcha_score = player.captcha_result

class Result(Page):
    pass


page_sequence = [Challenge, Result]
