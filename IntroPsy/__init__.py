from otree.api import *


doc = """
Introduction to Evolution Game
"""

from settings import BASE_PAY
from settings import MEAN_BONUS_PAY
from settings import MAX_NUM_ROUNDS
from settings import GROUP_SIZE
from settings import ENDOWMENT
from settings import FIXED_COST_PER_EXPERIMENT as FIXED_COST_PER_EXPERIMENT_SETTINGS
from settings import MAX_NUM_STUDIES



class C(BaseConstants):
    NAME_IN_URL = 'IntroPsy'
    PLAYERS_PER_GROUP =None
    GROUP_SIZE = GROUP_SIZE
    NUM_ROUNDS = 1
    BASE_PAY = BASE_PAY
    MEAN_BONUS_PAY = MEAN_BONUS_PAY
    MAX_NUM_ROUNDS = 1
    ENDOWMENT = ENDOWMENT
    FIXED_COST_PER_EXPERIMENT = FIXED_COST_PER_EXPERIMENT_SETTINGS
    MAX_NUM_STUDIES = MAX_NUM_STUDIES


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    pass
        
class Group(BaseGroup):
    
    item1 = models.StringField(label="")


class Player(BasePlayer):

    # now the psychological test
    
    Disatisfaction = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)], label = "satisfied/dissatisfied")
    NoEnergy = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "full of energy/without energy")
    Relaxed = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "stressed/relaxed")
    Awake = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "tired/wide awake")
    Angry = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "peaceful/angry")
    Happy = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "unhappy/happy")
    Motivated = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "unmotivated/highly motivated")
    Nervous = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "calm/nervous")
    Bored = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "enthusiastic/bored")
    NoWorry = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "worried/free of worry")



# PAGES
class Welcome(Page):
    pass


class AttentionAlertness(Page):
    form_model = "player"
    form_fields = ["Disatisfaction","NoEnergy","Relaxed","Awake","Angry","Happy","Motivated","Nervous","Bored","NoWorry"]

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass


page_sequence = [AttentionAlertness]
