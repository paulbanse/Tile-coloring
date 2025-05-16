from otree.api import *
import scipy.stats as ss

doc = """
This provides feedback to participants after the SampleSizeGame
"""

from settings import BASE_PAY
from settings import MEAN_BONUS_PAY
from settings import GROUP_SIZE
from settings import MAX_NUM_ROUNDS

class C(BaseConstants):
    NAME_IN_URL = 'Outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    BASE_PAY = BASE_PAY
    MEAN_BONUS_PAY = MEAN_BONUS_PAY
    GROUP_SIZE = GROUP_SIZE


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES

class Results(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        rank = player.participant.rank
        bonus = 0
        tied_count = 0
        tie = False
        for each_p in player.group.get_players():
            each_r = each_p.participant.rank
            if each_r == rank:
                tied_count += 1
        if tied_count == 1:
            tie = False
            factor = 2 ** rank
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE/factor
        elif rank - int(rank) == .5 and tied_count == 2:
            tie = True
            factor1 = 2 ** int(rank)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor1
            factor2 = 2 ** (int(rank) + 1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor2
        elif rank - int(rank) == .5 and tied_count == 4:
            tie = True
            factor1 = 2 ** (int(rank) - 1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor1
            factor2 = 2 ** (int(rank))
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor2
            factor3 = 2 ** (int(rank) + 1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor3
            factor4 = 2 ** (int(rank) + 2)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor4
        elif rank - int(rank) == 0 and tied_count == 3:
            tie = True
            factor1 = 2 ** (int(rank)-1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor1
            factor2 = 2 ** int(rank)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor2
            factor3 = 2 ** (int(rank) + 1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor3
        elif rank - int(rank) == 0 and tied_count == 5:
            tie = True
            factor1 = 2 ** (int(rank) - 2)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor1
            factor2 = 2 ** (int(rank) - 1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor2
            factor3 = 2 ** (int(rank))
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor3
            factor4 = 2 ** (int(rank) + 1)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor4
            factor5 = 2 ** (int(rank) + 2)
            bonus += C.MEAN_BONUS_PAY * C.GROUP_SIZE / factor5
        bonus = round(bonus/tied_count)

        player.participant.payoff = C.BASE_PAY + bonus
        return dict(rank = rank,
                    tie = tie,
                    cumulative_publications = player.participant.publications,
                    grants = player.participant.grants,
                    budget = player.participant.budget,
                    bonus = bonus,
                    reward = player.participant.payoff)

class End(Page):
    form_model = "player"
    @staticmethod
    def vars_for_template(player):
        rank = player.participant.rank
        reward = int(player.participant.payoff)
        return dict(reward = reward)

page_sequence = [Results,End]
