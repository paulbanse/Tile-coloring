from otree.api import *
from random import  randint

doc = """
Introduction to Evolution Game
"""


from settings import MAX_NUM_STUDIES
from settings import GROUP_SIZE
from settings import MAX_NUM_ROUNDS
from settings import NICHES as NICHES_SETTINGS
from settings import EFFECT_SIZE
from settings import ENDOWMENT
from settings import PERCENTAGE_SELECTION, NUMBER_STUDIES 
from settings import SCIENCE_VALUE

class C(BaseConstants):
    NAME_IN_URL = 'Tutorial'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ALPHA = 0.05
    ENDOWMENT = ENDOWMENT
    STUDY_IDS = range(1, MAX_NUM_STUDIES + 1)
    STR_PERCENTAGE = str(PERCENTAGE_SELECTION*100)
    NUMBER_STUDIES = NUMBER_STUDIES 

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    #import itertools
    #Iter = itertools.cycle([0,1,2, 3])
    for player in subsession.get_players():
        #val = next(Iter)
        player.participant.Science= SCIENCE_VALUE #val//2
        player.participant.vars["Science"] = SCIENCE_VALUE# player.participant.Science

        
class Group(BaseGroup):
    
    item1 = models.StringField(label="")


class Player(BasePlayer):
    Science = models.IntegerField(initial=-1)

    strSubList = models.LongStringField(initial = '0')
    totalclicks = models.IntegerField(initial=-1)
    letterList = models.LongStringField(initial = '')
    skipToComment = models.IntegerField(initial=-1)
    pass


# PAGES
class Welcome(Page):
    form_model = 'player'
    form_fields = ["skipToComment"]

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        player.participant.vars['skipToComment'] = player.skipToComment
        if player.skipToComment :
            return upcoming_apps[-1]

        

class Instructions(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(Science = player.participant.Science)
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars["Science"] = player.participant.Science
        player.Science = player.participant.Science

class FamiliarizationPart1(Page):
    form_model = 'player'
    form_fields = ['totalclicks',"strSubList","letterList","skipToComment"]

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        player.participant.vars['skipToComment'] = player.skipToComment
        if player.skipToComment :
            return upcoming_apps[-1]



class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass


page_sequence = [Instructions, Welcome,FamiliarizationPart1]
