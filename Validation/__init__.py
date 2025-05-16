from otree.api import *
from random import shuffle
import itertools
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
    NAME_IN_URL = 'Validation'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = MAX_NUM_ROUNDS
    ALPHA = 0.05
    ENDOWMENT = ENDOWMENT
    STUDY_IDS = range(1, MAX_NUM_STUDIES + 1)
    STR_PERCENTAGE = str(PERCENTAGE_SELECTION*100)
    NUMBER_STUDIES = NUMBER_STUDIES 

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):

    Iter = itertools.cycle([0,1,2, 3])
    for player in subsession.get_players():
        val = next(Iter)
        if not("Science" in player.participant.vars):
            player.participant.Science=SCIENCE_VALUE #val//2
            player.participant.sampleStart = randint(0,1) #val%2
        else :
            player.participant.Science= SCIENCE_VALUE #player.participant.vars["Science"]
            player.participant.sampleStart = randint(0,1) #val%2
        player.participant.offsetLatinSquare = randint(0,4)
            
        player.participant.grants = 0   #tells how much time they got published
        player.participant.achievedSampleFamiliarization = -1
        player.participant.achievedStudyFamiliarization = -1
        player.participant.achievedCombinedFamiliarization = -1
        
                
class Group(BaseGroup):
    
    item1 = models.StringField(label="")


class Player(BasePlayer):
    baseTarget = models.IntegerField(initial=-1)
    sampleStart = models.IntegerField(initial=-1)
    valueReached = models.IntegerField(initial=-1)
    strSubList = models.LongStringField(initial = '0')
    totalclicks = models.IntegerField(initial=-1)
    threshold = models.IntegerField(initial=-1)
    letterList = models.LongStringField(initial = '')
    theoreticalTarget = models.IntegerField(initial=-1)
    achievedSampleFamiliarization = models.IntegerField(initial=-1)
    achievedStudyFamiliarization = models.IntegerField(initial=-1)
    achievedCombinedFamiliarization = models.IntegerField(initial=-1)
    pass

# USEFULL FUNCTIONS

def LToClicksAndPubSample(L,sampleStart,filter):
    if filter == 7 or not(sampleStart):
        subList = [k for k in L if k>=filter]
        return(len(subList),subList)
    if sampleStart == 1:
        if len(L)>=filter:
            return(max(L),L)
        else: 
            return(0,[])

    

# PAGES

class Preparation(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(sampleStart = int(not(player.participant.sampleStart)), Science = player.participant.Science, RoundBoth = player.round_number >10) # notice here we do not use the sample start from the next round since it will be inversed
    def is_displayed(player):
        return (player.round_number % 5  == 1)
    def before_next_page(player: Player, timeout_happened):
        player.participant.sampleStart = int(not(player.participant.sampleStart))
        player.sampleStart = player.participant.sampleStart



class FamiliarizationPart2(Page):
    timeout_seconds = 30
    form_model = 'player'
    form_fields = ['totalclicks',"strSubList","letterList"]
    

    if Page.is_debug:
        timeout_seconds = 20

    def is_displayed(player):
        player.participant.vars["sampleStart"] = player.participant.sampleStart
        player.sampleStart = player.participant.sampleStart
        player.valueReached = 0
        Famlist = ["achievedSampleFamiliarization","achievedStudyFamiliarization","achievedCombinedFamiliarization"]

        for k in Famlist:
            setattr(player, k, player.participant.vars[k]) # we upload the past values
        return (player.round_number % 5  == 1)
    
    @staticmethod
    def js_vars(player):
        return dict(
            RoundBoth = player.round_number >10,
        )
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(sampleStart = player.participant.sampleStart,
                    Science = player.participant.Science, RoundBoth = player.round_number >10)
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        
        L = [int(k) for k in player.strSubList.split(";")]
        a,b = LToClicksAndPubSample(L,player.participant.sampleStart,1 + 6*(player.round_number>10))
        player.baseTarget = max(a,1)*2
        player.participant.pub_samples = b
        scale = [0.6,0.8,1,1.2,1.4]
        scalePlayer = [int(k*player.baseTarget) for k in scale][::-1]
        Offset = player.participant.offsetLatinSquare
        scalePlayer = scalePlayer[Offset:] + scalePlayer[:Offset]
        player.participant.vars["nextTasks"] = scalePlayer

        Famlist = ["achievedSampleFamiliarization","achievedStudyFamiliarization","achievedCombinedFamiliarization"]

        for k in Famlist:
            setattr(player, k, player.participant.vars[k]) # we upload the past values

        if player.round_number>10:
            test = (a>=2)
            ind = 2      
        elif player.participant.sampleStart == 1:
            test = (a>=19)
            ind = 0
        else:
            test = (a>=10)
            ind = 1
        test = int(test)
        player.participant.noCheat = test
        setattr(player, Famlist[ind],test)
        player.participant.vars[Famlist[ind]] = test #we change the new values

        if player.participant.noCheat == 0: #meaning they did not perform well enought
            player.baseTarget = -1
        else:
            player.strSubList = '0'
            player.totalclicks = -1
    


class Procedure(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(sampleStart = player.participant.sampleStart, Science = player.participant.Science, Threshold = int(player.participant.vars["nextTasks"][-1]), RoundBoth = player.round_number >10)
    def is_displayed(player):
        return (player.round_number % 5  == 1 and player.participant.noCheat)

    


class Validation(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = ['totalclicks',"strSubList","letterList"]
    if Page.is_debug:
        timeout_seconds = 10
    def is_displayed(player):
        return (player.participant.noCheat)
    @staticmethod
    def js_vars(player):
        return dict(
            RoundBoth = player.round_number >10,
        )
    @staticmethod
    def vars_for_template(player: Player):
        player.threshold = player.participant.vars["nextTasks"][-1]
        return dict(sampleStart = player.participant.sampleStart, Science = player.participant.Science, Threshold = int(player.participant.vars["nextTasks"][-1]), Round = (player.round_number-1)%5 +1 , RoundBoth = player.round_number >10)
         
    def before_next_page(player: Player, timeout_happened):
        L = [int(k) for k in player.strSubList.split(";")]
        a,b = LToClicksAndPubSample(L,player.participant.sampleStart,1 + 6*(player.round_number>10))
        player.valueReached = a 
        player.participant.pub_samples = b


class Results(Page):
    timeout_seconds = 60
    def is_displayed(player):
        return (player.participant.noCheat)
    def vars_for_template(player: Player):
        oldthreshold = int(player.participant.vars["nextTasks"][-1])
        player.participant.publications = int(player.valueReached >= oldthreshold) #tells if they published today
        grants = player.participant.publications + player.participant.grants
        resultDic = dict(sampleStart = player.participant.sampleStart,
                        Science = player.participant.Science, 
                        oldThreshold = oldthreshold , 
                        reached = player.participant.publications,
                        NbPublications = len(player.participant.pub_samples),
                        MaxPublication = max(player.participant.pub_samples+[0]),
                        Grants = grants,
                        Round = (player.round_number-1)%5 +1,
                        RoundBoth = player.round_number >10)
        if player.round_number % 5 != 0:
            resultDic['Threshold'] = int(player.participant.vars["nextTasks"][-2])
        else :
            resultDic['Threshold'] = 0  # here 0 on the threshold means there is no more threshold
        return resultDic
    def before_next_page(player: Player, timeout_happened):
        oldthreshold = int(player.participant.vars["nextTasks"].pop())
        player.participant.grants +=  int(player.valueReached >= oldthreshold)   #tells how much time they got published
        player.participant.vars["grant"] = player.participant.grants
    pass



page_sequence = [Preparation,FamiliarizationPart2,Procedure,Validation, Results]
