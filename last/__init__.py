from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'last'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    EDUCATION_LEVELS = [
        (1, "High school or less"),
        (2, "Some college"),
        (3, "Associates degree (for example: AA, AS)"),
        (4, "Bachelor’s degree (for example: BA. BS)"),
        (5, "Master’s degree (for example: MA, MS, MEng, MEd, MSW, MBA)"),
        (6, "Doctorate degree (for example, PhD, EdD)")
    ]

    INCOME_CHOICES = [
        (1, "under $15,000"),
        (2, "$15,000 - $24,999"),
        (3, "$25,000 - $34,999"),
        (4, "$35,000 - $49,999"),
        (5, "$50,000 - $74,999"),
        (6, "$75,000 - $99,999"),
        (7, "$100,000 - $149,999"),
        (8, "$150,000 - $199,999"),
        (9, "$200,000 and over")
    ]

    RACE_CHOICES = [
        (1, "White"),
        (2, "Black or African American"),
        (3, "Hispanic"),
        (4, "Asian"),
        (5, "American Indian or Alaska Native"),
        (6, "Other"),
        (7, "Prefer not to say")
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(min=18, max=100, label="How old are you?")
    gender = models.IntegerField(min=0, max=3, choices=[
        (1, 'Female'),
        (2, 'Male'),
        (3, 'Transgender'),
        (4, 'I use a different term'),
        (5, 'I prefer not to answer')

    ], label="What is your gender?", widget=widgets.RadioSelectHorizontal)
    race = models.IntegerField(label="What is your race?", choices=C.RACE_CHOICES)
    education_level = models.IntegerField(choices=C.EDUCATION_LEVELS,
                                          label="What is the highest degree or level of school you have completed?",
                                          widget=widgets.RadioSelect)
    education_major = models.StringField(label="If you have received at least some college education, what was your major?", blank=True)
    political_view = models.IntegerField(min=1, max=100)
    income_level = models.IntegerField(label="What is your gross annual income?", choices=C.INCOME_CHOICES)
    comment = models.LongStringField(label="Do you have any comments about the survey?", blank=True)

# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'race',
        'education_level',
        'education_major',
        'political_view',
        'income_level',
        'comment'
    ]
    
    def error_message(player, values):
        if values['education_level'] > 2 and values['education_major'] in [None, '']:
            return "Please specify your major if you have received at least an Associate's degree."

class LastPage(Page):
    pass



page_sequence = [Demographics, LastPage]
