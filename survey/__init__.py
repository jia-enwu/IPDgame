from otree.api import *

doc = """
This survey asks participants about their attitudes toward public service, citizenship, compassion, self-sacrifice, and basic demographic information.
"""

class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # APS: Attitudes toward Public Service
    APS5 = models.IntegerField(label="I admire people who initiate or are involved in activities to aid my community.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    APS7 = models.IntegerField(label="It is important to contribute to activities that tackle social problems.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    CP11 = models.IntegerField(label="Meaningful public service is very important to me.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    CP12 = models.IntegerField(label="It is important for me to contribute to the common good.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)

    # CPV: Citizenship and Public Values
    CPV1 = models.IntegerField(label="I think equal opportunities for citizens are very important.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    CPV2 = models.IntegerField(label="It is important that citizens can rely on the continuous provision of public services.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    CPV6 = models.IntegerField(label="It is fundamental that the interests of future generations are taken into account when developing public policies.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    CPV7 = models.IntegerField(label="To act ethically is essential for public servants.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)

    # COM: Compassion
    COM2 = models.IntegerField(label="I feel sympathetic to the plight of the underprivileged.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    COM3 = models.IntegerField(label="I empathize with other people who face difficulties.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    COM5 = models.IntegerField(label="I get very upset when I see other people being treated unfairly.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    COM6 = models.IntegerField(label="Considering the welfare of others is very important.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)

    # SS: Self-Sacrifice
    SS2 = models.IntegerField(label="I am prepared to make sacrifices for the good of society.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    SS3 = models.IntegerField(label="I believe in putting civic duty before self.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    SS4 = models.IntegerField(label="I am willing to risk personal loss to help society.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)
    SS7 = models.IntegerField(label="I would agree to a good plan to make a better life for the poor, even if it costs me money.", choices=[
        (1, "Strongly Disagree"),
        (2, "Disagree"),
        (3, "Neutral"),
        (4, "Agree"),
        (5, "Strongly Agree")
    ], widget=widgets.RadioSelect)

    # Demographics
    age = models.IntegerField(label="What is your age?", min=18, max=99)
    gender = models.StringField(
        label="What is your gender?",
        choices=["Male", "Female", "Non-binary/Third gender", "Prefer not to say"],
        widget=widgets.RadioSelect
    )
    race = models.StringField(
        label="What is your race?",
        choices=["White", "Black or African American", "Asian", "Hispanic or Latino", "Native American", "Other", "Prefer not to say"],
        widget=widgets.RadioSelect
    )
    econ_class = models.StringField(
        label="Have you ever taken an economics class?",
        choices=["Yes", "No"],
        widget=widgets.RadioSelect
    )
    active_role = models.IntegerField(
        label="How capable do you think you are in taking an active role in the game you just finished?", 
        choices=[
            (1, "Not at all able"),
            (2, "A little able"),
            (3, "Quite able"),
            (4, "Very able"),
            (5, "Completely able")
        ], 
        widget=widgets.RadioSelect
    )
    confidence = models.IntegerField(
        label="How confident are you in your ability to play the game you just finished?", 
        choices=[
            (1, "Not at all confident"),
            (2, "A little confident"),
            (3, "Quite confident"),
            (4, "Very confident"),
            (5, "Completely confident")
        ], 
        widget=widgets.RadioSelect
    )

# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = [
        'APS5', 'APS7', 'CP11', 'CP12',
        'CPV1', 'CPV2', 'CPV6', 'CPV7',
        'COM2', 'COM3', 'COM5', 'COM6',
        'SS2', 'SS3', 'SS4', 'SS7'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'scale_description': "Please answer the following questions on a scale from 1 to 5, where 1 means 'Strongly Disagree' and 5 means 'Strongly Agree'."
        }

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'race', 'econ_class', 'active_role', 'confidence']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'instructions': "Please provide some basic demographic information about yourself."
        }

page_sequence = [Survey, Demographics]
