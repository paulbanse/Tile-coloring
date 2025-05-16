from otree.api import *


doc = """
Introduction to Evolution Game
"""

from settings import BASE_PAY
from settings import LOOSER_PAY
from settings import MEAN_BONUS_PAY
from settings import MAX_NUM_ROUNDS
from settings import GROUP_SIZE
from settings import ENDOWMENT
from settings import FIXED_COST_PER_EXPERIMENT as FIXED_COST_PER_EXPERIMENT_SETTINGS
from settings import MAX_NUM_STUDIES



class C(BaseConstants):
    NAME_IN_URL = 'Intro'
    PLAYERS_PER_GROUP =None
    GROUP_SIZE = GROUP_SIZE
    NUM_ROUNDS = 1
    LOOSER_PAY = LOOSER_PAY
    BASE_PAY = BASE_PAY
    MEAN_BONUS_PAY = MEAN_BONUS_PAY
    MAX_NUM_ROUNDS = MAX_NUM_ROUNDS
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
    age = models.IntegerField(label="Please enter your age.",
                              min=18,max=90)
    gender = models.StringField(label="Please indicate your gender.",
                                choices=["male", "female", "other", "prefer not to say"])
    experience = models.StringField(label='Please indicate your highest education level.',
                                    choices=['Primary school', "Secondary school up to 16 years", 
                                            "Higher or secondary or further education",
                                            'College or university',
                                            'Post-graduate degree'])
    occupation = models.StringField(label='Please indicate your occupation',
                                    choices=[ "student", 'researcher', "other" ])
    
    # Prolific ID
    
    prolificID = models.LongStringField(label = "Please indicate your Prolific ID", initial = '')




# PAGES
class Welcome(Page):
    def vars_for_template(player: Player):
        
        return dict( MinimumKick = C.LOOSER_PAY,  Minimum = C.BASE_PAY, Maximum = C.BASE_PAY + C.MEAN_BONUS_PAY * 15, Bonus = C.MEAN_BONUS_PAY)
    pass

class Demographics(Page):
    form_model = "player"
    form_fields = ["age", "gender",'experience','occupation']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.age = player.age
        player.participant.gender = player.gender
        player.participant.occupation = player.occupation
        player.participant.experience = player.experience

        
class ProId(Page):
    form_model = "player"
    form_fields = ["prolificID"]

class ResultsWaitPage(WaitPage):
    pass

class Results(Page):
    pass


page_sequence = [ProId, Welcome, Demographics]
