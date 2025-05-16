from otree.api import *
import statsmodels.stats.power as getpower
import random
import numpy as np
import scipy.stats as ss

doc = """
App to choose sample sizes and estimate plausible resultant publication rates and incomes.
Participants start with an initial endowment/budget, which the can allocate to experiments by choosing sample sizes.
We will use empirical values of prior probability and effect size to calculate the total income from publications
(publishable findings = true positive findings + false positive findings).

In the next round the cost of experimentation is subtracted and the income from publication is added to your budget.
You can proceed to allocate samples, either building a publication record or going bankrupt.

"""
'''
ssh administrator@web52.bonneconlab.uni-bonn.de
server web52.bonneconlab.uni-bonn.de
'''

from settings import MAX_NUM_STUDIES
from settings import GROUP_SIZE
from settings import MAX_NUM_ROUNDS
from settings import NICHES as NICHES_SETTINGS
from settings import EFFECT_SIZE
from settings import ENDOWMENT
from settings import PERCENTAGE_SELECTION, NUMBER_STUDIES 
from settings import TIMER

class C(BaseConstants):
    NAME_IN_URL = 'Evolution'
    PLAYERS_PER_GROUP = GROUP_SIZE
    NUM_ROUNDS = MAX_NUM_ROUNDS
    ALPHA = 0.05
    ENDOWMENT = ENDOWMENT
    NICHES = NICHES_SETTINGS
    STUDY_IDS = range(1, MAX_NUM_STUDIES + 1)
    EFFECT_SIZE = EFFECT_SIZE
    PERCENTAGE_SELECTION = PERCENTAGE_SELECTION
    STR_PERCENTAGE = str(PERCENTAGE_SELECTION*100)
    NUMBER_STUDIES = NUMBER_STUDIES 


class Subsession(BaseSubsession):
    locked = models.BooleanField(initial=False)
    #generation = models.IntegerField(initial=0)

def creating_session(subsession: Subsession):
    ''' participants should be subdivided into two groups or niches'''
    if subsession.round_number ==1:
        #subsession.group_randomly()
        for group in subsession.get_groups():
            group.niche = C.NICHES[0]
            print('the base rate is %.2f' %group.niche)
            for player in group.get_players():
                participant = player.participant
                participant.niche = group.niche
                participant.theory = 0
                participant.publications = 0
                #participant.relative_pubs = 1/C.PLAYERS_PER_GROUP
                participant.pub_samples = []
                participant.pub_sample_rounds = []
                participant.all_samples = []
                participant.all_sample_rounds = []
                participant.studyList = [0 for k in range(C.NUMBER_STUDIES)]
                participant.rank = 0
                participant.Avgtheory = 0
    else:
        subsession.group_like_round(1)

    #random.seed(42)
    #session = subsession.session
    #session.history = []

class Group(BaseGroup):
    niche = models.FloatField()
    winner1 = models.IntegerField(initial=0)
    winner2 = models.IntegerField(initial=0)
    year = models.IntegerField(initial=0)

    @staticmethod
    def get_cumulative_pubs(group):
        id_list = []
        pub_list = []
        for p in group.get_players():
            id_list.append(p.id_in_group)
            pub_list.append(p.participant.publications)
        return (id_list, pub_list)
'''
    @staticmethod
    def get_recent_pubs(group):
        id_list = []
        pub_list = []
        for p in group.get_players():
            id_list.append(p.id_in_group)
            #pub_list.append(p.participant.publications)
            pub_list.append(p.participant.recent_pubs)
        return (id_list, pub_list)

    @staticmethod
    def get_mean_cost(group):
        total = 0
        for p in group.get_players():
            total += p.participant.budget
        mean_current_budget = total / C.PLAYERS_PER_GROUP
        mean_cost = C.ENDOWMENT - int(mean_current_budget)
        #group.mean_cost = mean_cost
        group.mean_cost = C.PLAYERS_PER_GROUP * 50
'''

class Player(BasePlayer):
    
    button_clicks = models.IntegerField(initial=0)  #TODO take these off
    link_clicks = models.IntegerField(initial=0)
    
    publication = models.BooleanField(initial=False)
    publications = models.IntegerField(initial=0)
    niche = models.FloatField()
    recent_pubs = models.IntegerField(initial=0)
    theory = models.IntegerField(initial=0)
    Avgtheory = models.FloatField(initial = 0)
    strSubList = models.LongStringField(initial = '')
    
    
    def update(player):
        p = player
        b0 = C.NICHES[0]
        b1  = C.NICHES[1]
        e = p.participant.theory
        p.participant.niche = (b0 + b1 * (e))/(e+1)
        ss_list = p.participant.studyList
        #publication_rate=0
        print(ss_list, p.participant.niche)
        for s in ss_list:
            probability_of_publication = get_publication_rate(s,p.participant.niche)

            p.participant.all_samples.append(s)
            p.participant.all_sample_rounds.append(p.round_number)
            
            if np.random.rand() < probability_of_publication:
                p.publications += 1
                p.participant.pub_samples.append(s)
                p.participant.pub_sample_rounds.append(p.round_number)
                p.publication = True
                #publication_rate += probability_of_publication
        #print('%i studies with %i samples yields a total publication rate of %.2f per year'%(len(ss_list), np.mean(ss_list), publication_rate))
        p.participant.publications += p.publications
        p.participant.Avgtheory += (p.participant.theory - p.participant.Avgtheory)/p.round_number
        
        p.participant.studyList = [0 for k in range(C.NUMBER_STUDIES)]
        p.participant.theory = 0
        '''
        if p.round_number == 3:
            list = p.in_rounds((p.round_number-2), p.round_number)
            p.participant.recent_pubs  = sum([p.publications for p in list])
        elif p.round_number == 4:
            p.participant.recent_pubs = sum(
                [p.publications for p in p.in_rounds(p.round_number - 3, p.round_number)])
        elif p.round_number > 4:
            p.participant.recent_pubs = sum(
                [p.publications for p in p.in_rounds(p.round_number - 4, p.round_number)])
        '''



def get_publication_rate(s,b):
    if s == 0:
        return 0
    else:
        analysis = getpower.TTestIndPower()
        # median effect size from Szucs2017 =0.93, mean~0.5
        Power = analysis.solve_power(effect_size=C.EFFECT_SIZE, nobs1=s, ratio=1.0, alpha=C.ALPHA, power=None,
                                    alternative='two-sided')

        falsePR = C.ALPHA * (1 - b)
        truePR = Power * b
        publication_rate = falsePR + truePR
        return publication_rate

# PAGES
class GBAT(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Wait(WaitPage):
    body_text = "You are in the queue..."

    @staticmethod
    def after_all_players_arrive(group: Group):
        subsession = group.subsession
        subsession.locked = True
        '''
        if group.round_number > 3:
            ## grant probabitliy based on pub-count (cardinal fitness)
            #(ids, pubs) = group.get_recent_pubs(group)
            #if sum(pubs)>0:
            #    weights = np.array(pubs)/sum(pubs)
            #    w1,w2 = np.random.choice(np.array(ids), size=2, p=weights)
            #else:
                w1 = w2 = 0
            group.winner1 = int(w1)
            group.winner2 = int(w2)
            group.get_mean_cost(group)
        '''
        for i,p in enumerate(group.get_players()):
            # draw winners
            '''
            if group.winner1 == p.id_in_group:
                #p.income += group.mean_cost
                p.participant.grants += 1
            if group.winner2 == p.id_in_group:
                #p.income += group.mean_cost
                p.participant.grants += 1
            if p.id_in_group != group.winner1 and p.id_in_group != group.winner2:
                pass
                #p.income = 0
            
            # pay per publication
            if p.publication:
                p.participant.grants += 1
            '''
            (ids, allpubs) = group.get_cumulative_pubs(group)
            #relative_pubs = np.array(allpubs) / sum(allpubs)
            reverse_pubs = [-p for p in allpubs]
            ranks = ss.rankdata(reverse_pubs, method='average')
            if p.id_in_group == ids[i]:
                #p.participant.relative_pubs = relative_pubs[i]
                rank = ranks[i]
                if rank - int(rank) == 0:
                    rank = int(rank)
                p.participant.rank = rank


class Choice(Page):
    if TIMER:
        timeout_seconds = 90


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.update()
        #player.relative_pubs = player.participant.relative_pubs

    @staticmethod
    def live_method(player: Player, data):
        print(player.id_in_group, data)
        L = [int(k) for k in data.split(";")]  
        if L[0]== 0:
            player.participant.studyList = L 
        else:
            player.participant.theory = L[0]
        player.strSubList = data[2:]

        

        
        
class Results(Page):
    form_model = 'player'
    
    if not(Page.is_debug):
        timeout_seconds = 2 * 60 
        
    @staticmethod
    def vars_for_template(player):
        if player.publications > 0:
            player.publication = True
        rank = player.participant.rank
        if rank-int(rank) == 0:
            #rank = int(rank)
            tie = False
        else:
            tie = True
        rankList = [(k.participant.rank,k.id_in_group,k.participant.Avgtheory, k) for k in player.get_others_in_group() ] + [(player.participant.rank,player.id_in_group,player.participant.Avgtheory,player)]
        rankList.sort()
        playersRanked = [k[3] for k in rankList]
        theoriesRanked = [k[2] for k in rankList]
        lastRankSelected = int(PERCENTAGE_SELECTION* len(playersRanked ))+1
        lastSelected = [ k[3] for k in rankList if k[0] < lastRankSelected][-1]
        return dict(tie=tie,
                    rank=rank,
                    new_publications=player.publications,
                    cumulative_publications = player.participant.publications,
                    theoriesRanked = theoriesRanked,
                    playersRanked = playersRanked,
                    lastSelected = lastSelected)

page_sequence = [GBAT, Choice, Wait, Results]
