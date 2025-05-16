from os import environ, popen

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ENDOWMENT = 20000
MAX_NUM_STUDIES = 30
BASE_PAY = 3.75
LOOSER_PAY = 1.00
MEAN_BONUS_PAY = 0.50
MAX_NUM_ROUNDS = 15
GROUP_SIZE = 4
NICHES = [0.01,0.25]
FIXED_COST_PER_EXPERIMENT = [2,20]
EFFECT_SIZE = 0.5
PERCENTAGE_SELECTION = 0.5
NUMBER_STUDIES = 20
TIMER = True
SCIENCE_VALUE = 0
#CONDITION = 'BeGood'
#CONDITION = 'BeCompetitive'

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=4.00,
    doc="",
    max_num_studies=MAX_NUM_STUDIES,
    base_pay = BASE_PAY,
    mean_bonus_pay = MEAN_BONUS_PAY,
    max_round_number = MAX_NUM_ROUNDS,
    group_size = GROUP_SIZE,
    python_version = popen('python3 --version').read().strip(),
    pip_freeze = popen('pip3 freeze').read().strip().replace("\n", " | "),
    niches = NICHES,
    fixed_cost_per_experiment = FIXED_COST_PER_EXPERIMENT,
    theory = 0,
    Avgtheory = 0,
    percentage_selection = PERCENTAGE_SELECTION,
    number_studies = NUMBER_STUDIES
)
#
SESSION_CONFIGS = [
    dict(
        name='Validation',
        app_sequence=['Intro','IntroPsy','Tutorial','Validation',"OutroPsy"],
        num_demo_participants=GROUP_SIZE,
        theory=0,
    ),
    dict(
        name='SampleSizeGameB',
        app_sequence=['Intro', 'Evolution', 'Outro'],
        num_demo_participants=GROUP_SIZE,
        theory=1,
    ),
    dict(
        name='Evolution',
        app_sequence=['Evolution','Outro'],
        num_demo_participants=GROUP_SIZE,
        theory=0
    ),
    dict(
        name='Intro',
        app_sequence=['Intro','IntroPsy','Tutorial'],
        num_demo_participants=2,
    ),
    dict(
        name='Test',
        app_sequence=['Tutorial'],
        num_demo_participants=4,
    ),
]

PARTICIPANT_FIELDS = ['age', 'gender', 'occupation', 'experience', 'niche','theory','publications','Avgtheory',
                      'recent_pubs', 'relative_pubs','pub_samples', 'pub_sample_rounds','all_samples','all_sample_rounds',
                      'grants','rank','studyList',"Science","clicks","sampleStart",'nextTasks','id_in_group','valueReached',
                      "noCheat","offsetLatinSquare", 'achievedSampleFamiliarization','achievedStudyFamiliarization','achievedCombinedFamiliarization','skipToComment']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [
    dict(
        name = 'SSG',
        display_name = 'Room without participant labels',
        #participant_label_file = _rooms/X.txt,
    )
]

ADMIN_USERNAME = 'admin-meta'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6808502147057'
