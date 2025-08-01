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
        headers = dict(self.request.headers)
        headers_lower = dict()
        for k, v in headers.items():
            k_l = k.replace('-', '_')
            headers_lower[k_l] = v
        ctx['headers'] = headers_lower
        
        openai_signatures = {
            'signature': None,
            'signature_input': None,
            'signature_agent': None
        }
        
        if 'signature' in headers_lower:
            openai_signatures["signature"] = headers_lower['signature']
        if 'signature_input' in headers_lower:
            openai_signatures["signature_input"] = headers_lower['signature_input']
        if 'signature_agent' in headers_lower:
            openai_signatures['signature_agent'] = headers_lower['signature_agent']
        
        ctx.update(**openai_signatures)
        
        return ctx


class Results(Page):
    pass


page_sequence = [MyPage, Results]
