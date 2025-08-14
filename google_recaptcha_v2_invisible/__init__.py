from otree.api import *
from otree import settings
import requests 
import json 

doc = """
Your app description
"""

def validate_token(token, secret):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {'secret': secret, 'response': token }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Token validation error: {e}")
        return {'success': False, 'error-codes': ['internal-error']}


class C(BaseConstants):
    NAME_IN_URL = 'grc2i'
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
    captcha_result = models.BooleanField()
    captcha_server_response = models.LongStringField()

    consent_given = models.BooleanField(initial=False,
                                        label="I am 18 years or older, have read the above information and I consent to participate in this study",
                                        widget=widgets.CheckboxInput)

# PAGES
class Challenge(Page):
    form_model = 'player'
    form_fields = ['consent_given', 'captcha_token']
    
    def vars_for_template(player):
        return {
            'captcha_site_key': settings.G4_SITE_KEY,
        }

def captcha_token_error_message(player, value):
    if not value:
        return 'Please complete the challenge.'
    
    result = validate_token(value, settings.G4_SECRET_KEY)
    player.captcha_server_response = json.dumps(result)
    player.captcha_result = result.get('success', False)
    player.captcha_score = 1 if player.captcha_result else 0
    return None
        

class Result(Page):
    pass


page_sequence = [Challenge, Result]
