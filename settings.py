from os import environ

SESSION_CONFIGS = [
    dict(
        name='experiment',
        app_sequence=['irpd_game_1','irpd_game_2', 'irpd_game_3', 'irpd_game_4', 'irpd_game_5', 'survey'],
        num_demo_participants=2,
        display_name='IRPD Game - 5 Iterations with Survey',
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9648494621304'