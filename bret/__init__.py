from otree.api import *
import random

author = 'Felix Holzmeister & Armin Pfurtscheller, adapted by Christian König (2025)'

doc = """
Bomb Risk Elicitation Task (BRET) à la Crosetto/Filippin (2013), Journal of Risk and Uncertainty (47): 31-65.
"""

class C(BaseConstants):

    # oTree C
    NAME_IN_URL = 'bret'
    PLAYERS_PER_GROUP = None

    # value of single collected box
    BOX_VALUE = cu(0.1)

    # number of rows and columns
    NUM_ROWS = 8
    NUM_COLS = 8

    # box height and box width in pixels
    BOX_HEIGHT = '50px'
    BOX_WIDTH = '50px'

    # number of rounds to be played
    NUM_ROUNDS = 1

    # determines whether all rounds played are payed-off or whether one round is randomly chosen for payment
    # only matters if round number is > 1
    RANDOM_PAYOFF = True

    # show instruction page
    INSTRUCTIONS = True

    # show FEEDBACK by resolving boxes, i.e. toggle boxes and show whether bomb was collected or not
    # if true the button "Solve" will be rendered and active after game play ends ("Stop")
    FEEDBACK = True

    # show RESULTS page summarizing the game outcome
    RESULTS = False

    # "DYNAMIC" or "static" game play
    DYNAMIC = True

    # time interval between single boxes being collected (in seconds)
    # note that this only affects game play if <DYNAMIC = True>
    TIME_INTERVAL = 1.00

    # collect boxes randomly or in order
    RANDOM_COLLECTION = False

    # determines whether static game play allows for selecting boxes by clicking or by entering a number
    # if <DEVILS_GAME = True>, game play is similar to Slovic (1965), i.e. boxes are collected by subjects
    # if <DEVILS_GAME = False>, subjects enter the number of boxes they want to collect
    # note that this only affects game play if <DYNAMIC = False>
    DEVILS_GAME = False

    # determine whether boxes can be toggled only once or as often as clicked
    UNDOABLE = False


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # whether bomb is collected or not
    # store as integer because it's easier for interop with JS
    bomb = models.IntegerField()

    # location of bomb
    bomb_row = models.PositiveIntegerField()
    bomb_col = models.PositiveIntegerField()

    # number of collected boxes
    boxes_collected = models.IntegerField()

    # --- set round RESULTS and player's payoff
    pay_this_round = models.BooleanField()
    round_result = models.CurrencyField()

    def set_payoff(player):

        # determine round_result as (potential) payoff per round
        if player.bomb:
            player.round_result = cu(0)
        else:
            player.round_result = player.boxes_collected * C.BOX_VALUE

        # set payoffs if <RANDOM_PAYOFF = True> to round_result of randomly chosen round
        # randomly determine round to pay on player level
        if player.subsession.round_number == 1:
            player.participant.vars['round_to_pay'] = random.randint(1, C.NUM_ROUNDS)

        if C.RANDOM_PAYOFF:
            if player.subsession.round_number == player.participant.vars['round_to_pay']:
                player.pay_this_round = True
                player.payoff = player.round_result
            else:
                player.pay_this_round = False
                player.payoff = cu(0)

        # set payoffs to round_result if <RANDOM_PAYOFF = False>
        else:
            player.payoff = player.round_result


# FUNCTIONS

# BRET settings for Javascript application
def common_vars_for_template(player):
    reset = player.participant.vars.get('reset',False)
    if reset:
        del player.participant.vars['reset']

    input = not C.DEVILS_GAME if not C.DYNAMIC else False

    otree_vars = {
        'reset':            reset,
        'input':            input,
        'random_collection':           C.RANDOM_COLLECTION,
        'dynamic':          C.DYNAMIC,
        'num_rows':         C.NUM_ROWS,
        'num_cols':         C.NUM_COLS,
        'feedback':         C.FEEDBACK,
        'undoable':         C.UNDOABLE,
        'box_width':        C.BOX_WIDTH,
        'box_height':       C.BOX_HEIGHT,
        'time_interval':    C.TIME_INTERVAL,
    }

    return {
        'otree_vars':       otree_vars
    }

# PAGES
class Instructions(Page):

    # only display instruction in round 1
    def is_displayed(player):
        return player.round_number == 1

    # variables for use in template
    def vars_for_template(player):
        return {
            'num_rows':             C.NUM_ROWS,
            'num_cols':             C.NUM_COLS,
            'num_boxes': C.NUM_ROWS * C.NUM_COLS,
            'num_nobomb': C.NUM_ROWS * C.NUM_COLS - 1,
            'box_value':            C.BOX_VALUE,
            'time_interval':        C.TIME_INTERVAL,
        }


class Decision(Page):
    # form fields on player level
    form_model = 'player'
    form_fields = [
        'bomb',
        'boxes_collected',
        'bomb_row',
        'bomb_col',
    ]

    def vars_for_template(player):
        return common_vars_for_template(player)
    
    def js_vars(player):
        return common_vars_for_template(player)

    def before_next_page(player, timeout_happened):
        player.participant.vars['reset'] = True
        player.set_payoff()


class Results(Page):

    # only display RESULTS after all rounds have been played
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    # variables for use in template
    def vars_for_template(player):
        total_payoff = sum([p.payoff for p in player.in_all_rounds()])
        player.participant.vars['bret_payoff'] = total_payoff

        return {
            'player_in_all_rounds':   player.in_all_rounds(),
            'box_value':              C.BOX_VALUE,
            'boxes_total': C.NUM_ROWS * C.NUM_COLS,
            'boxes_collected':        player.boxes_collected,
            'bomb':                   player.bomb,
            'bomb_row':               player.bomb_row,
            'bomb_col':               player.bomb_col,
            'round_result':           player.round_result,
            'round_to_pay':           player.participant.vars['round_to_pay'],
            'payoff':                 player.payoff,
            'total_payoff':           total_payoff,
        }



page_sequence = [Decision]

if C.INSTRUCTIONS:
    page_sequence.insert(0,Instructions)

if C.RESULTS:
    page_sequence.append(Results)
