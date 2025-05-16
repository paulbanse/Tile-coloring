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
    NAME_IN_URL = 'OutroPsy'
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
    for player in subsession.get_players():
        if not("grant" in player.participant.vars):
            player.participant.grants = 0
        else:
            player.participant.grants = player.participant.vars["grant"]
    pass
        
class Group(BaseGroup):
    
    item1 = models.StringField(label="")


class Player(BasePlayer):
    # motivation
    
    JoyInTask = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)], label = "The fulfillment/completion of the task itself was already fun.")
    EarnMoney = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "I wanted to make/earn as much money as possible.")
    MeetExperimenterExpectations  = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "I wanted to meet the expectations of the experimenter, who surely expected my commitment.")
    DiligentAttitude  = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "I am a hardworking person and do everything diligently and with commitment.")


    # attention alertness
    
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

    # Perception measure
    
    NoFun = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)], label = "was fun|did not bring joy")
    NoFeedback = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "gave me a target/ performance measurement that motivated me|did not give me any feedback")
    Boring = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "aroused my curiosity/ was entertaining|was very uninteresting/ boring")
    Tedious = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "was appealing/ effortlessly manageable|was very tedious/ annoying/ tiring")
    Meaningless = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "appeared to be meaningful|seemed pointless")
    PhysicallyDemanding = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "was physically easy|was physically demanding/ exhausting")
    MentallyDemanding = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "was mentally easy|was mentally demanding/ exhausting")
    NoOutcome = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "produces something/ achieves a goal|produces nothing/ has no measurable result")
    
    # Performance
    
    Performance = models.IntegerField(widget=widgets.RadioSelect,choices = [k for k in range(1,8)],label = "not at all|completely")
    
    # Comment page
    
    Comment = models.LongStringField(initial = '')
    Mouse = models.BooleanField(choices=[[False, 'No'],[True, 'Yes'],],label = "Did you use an external mouse ?")

# PAGES

class Motivation(Page):
    def is_displayed(player):
        return (not player.participant.skipToComment)
    form_model = "player"
    form_fields = ["JoyInTask","EarnMoney","MeetExperimenterExpectations","DiligentAttitude" ]

class AttentionAlertness(Page):
    def is_displayed(player):
        return (not player.participant.skipToComment)
    form_model = "player"
    form_fields = ["Disatisfaction","NoEnergy","Relaxed","Awake","Angry","Happy","Motivated","Nervous","Bored","NoWorry"]

class Perception(Page):
    def is_displayed(player):
        return (not player.participant.skipToComment)
    form_model = "player"
    form_fields = ["NoFun","NoFeedback","Boring","Tedious","Meaningless","PhysicallyDemanding","MentallyDemanding","NoOutcome"]
    
class Performance(Page):
    def is_displayed(player):
        return (not player.participant.skipToComment)
    form_model = "player"
    form_fields = ["Performance"]
    
class Comments(Page):
    form_model = "player"
    form_fields = ["Comment",'Mouse']

class Ending(Page):
    def is_displayed(player):
        return (not player.participant.skipToComment)
    timeout_seconds = 120
    def vars_for_template(player: Player):
        player.participant.payoff = MEAN_BONUS_PAY * player.participant.grants


page_sequence = [Motivation,AttentionAlertness,Perception,Performance,Comments,Ending]
