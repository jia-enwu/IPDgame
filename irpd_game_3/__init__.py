from otree.api import *

doc = """
Game 2: This game continues with players in their respective treatment or control groups as assigned in Game 1.
"""

import random

class C(BaseConstants):
    NAME_IN_URL = 'irpd_game_3'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 20
    StopProbability = 50

    # Payoff matrix for control group (Game 1)
    PayoffCC_control = 65
    PayoffCD_control = 10
    PayoffDC_control = 100
    PayoffDD_control = 35

    # Payoff matrix for treatment group (Game 2)
    PayoffCC_treatment = 75
    PayoffCD_treatment = 10
    PayoffDC_treatment = 100
    PayoffDD_treatment = 45


class Subsession(BaseSubsession):
    def creating_session(self):
        # No need to reassign treatment/control; use the value from Game 1
        for player in self.get_players():
            # Ensure the treatment assignment is preserved from Game 1
            assert 'treatment' in player.participant.vars, "Treatment assignment missing from participant.vars"

        # Create separate lists for treatment and control participants
        treatment_players = [p for p in self.get_players() if p.participant.vars['treatment'] == 'treatment']
        control_players = [p for p in self.get_players() if p.participant.vars['treatment'] == 'control']

        # Shuffle players in each group to ensure random pairing within treatment/control groups
        random.shuffle(treatment_players)
        random.shuffle(control_players)

        # Assign groups based on treatment or control group assignment
        group_matrix = []

        # Split treatment players into pairs
        for i in range(0, len(treatment_players), C.PLAYERS_PER_GROUP):
            group_matrix.append(treatment_players[i:i + C.PLAYERS_PER_GROUP])

        # Split control players into pairs
        for i in range(0, len(control_players), C.PLAYERS_PER_GROUP):
            group_matrix.append(control_players[i:i + C.PLAYERS_PER_GROUP])

        # Set the group matrix for the subsession
        self.set_group_matrix(group_matrix)


class Player(BasePlayer):
    decision = models.StringField(
        choices=[
            ('C', 'Cooperate with the university'),
            ('D', 'Refuse to cooperate with the university')
        ],
        widget=widgets.RadioSelect
    )

    @property
    def treatment(self):
        return self.participant.vars['treatment']


class Group(BaseGroup):
    stopped_early = models.BooleanField(initial=False)
    number = models.IntegerField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['decision']

    @staticmethod
    def is_displayed(player: Player):
        return not player.group.stopped_early

    @staticmethod
    def vars_for_template(player: Player):
        # Determine the payoffs based on the player's group
        if player.treatment == 'treatment':
            return {
                'payoff_CC': C.PayoffCC_treatment,
                'payoff_CD': C.PayoffCD_treatment,
                'payoff_DC': C.PayoffDC_treatment,
                'payoff_DD': C.PayoffDD_treatment,
                'group': 'Treatment'
            }
        else:
            return {
                'payoff_CC': C.PayoffCC_control,
                'payoff_CD': C.PayoffCD_control,
                'payoff_DC': C.PayoffDC_control,
                'payoff_DD': C.PayoffDD_control,
                'group': 'Control'
            }


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        p1 = group.get_players()[0]
        p2 = group.get_players()[1]

        # Assign payoffs based on treatment or control group
        if p1.treatment == 'treatment':
            # Treatment group (Game 2 payoff matrix)
            if p1.decision == 'C' and p2.decision == 'C':
                p1.payoff = C.PayoffCC_treatment
                p2.payoff = C.PayoffCC_treatment
            elif p1.decision == 'C' and p2.decision == 'D':
                p1.payoff = C.PayoffCD_treatment
                p2.payoff = C.PayoffDC_treatment
            elif p1.decision == 'D' and p2.decision == 'C':
                p1.payoff = C.PayoffDC_treatment
                p2.payoff = C.PayoffCD_treatment
            elif p1.decision == 'D' and p2.decision == 'D':
                p1.payoff = C.PayoffDD_treatment
                p2.payoff = C.PayoffDD_treatment
        else:
            # Control group (Game 1 payoff matrix)
            if p1.decision == 'C' and p2.decision == 'C':
                p1.payoff = C.PayoffCC_control
                p2.payoff = C.PayoffCC_control
            elif p1.decision == 'C' and p2.decision == 'D':
                p1.payoff = C.PayoffCD_control
                p2.payoff = C.PayoffDC_control
            elif p1.decision == 'D' and p2.decision == 'C':
                p1.payoff = C.PayoffDC_control
                p2.payoff = C.PayoffCD_control
            elif p1.decision == 'D' and p2.decision == 'D':
                p1.payoff = C.PayoffDD_control
                p2.payoff = C.PayoffDD_control

        # Generate a random number to determine if the game should stop early
        group.number = random.randint(0, 100)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return {
            'my_decision': player.decision,
            'other_decision': other_player.decision,
            'payoff': player.payoff,
        }

    @staticmethod
    def is_displayed(player: Player):
        return not player.group.stopped_early

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Determine if the game should stop early or if it's the last round
        if player.group.number < C.StopProbability or player.round_number == C.NUM_ROUNDS:
            player.group.stopped_early = True


class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Display FinalResults page only if the game has stopped early or reached the last round
        return player.group.stopped_early

    @staticmethod
    def vars_for_template(player: Player):
        total_payoff = sum([p.payoff for p in player.in_all_rounds()])
        return {
            'total_payoff': total_payoff,
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        # After displaying the FinalResults, go to the next app in the session config
        return upcoming_apps[0] if upcoming_apps else None


page_sequence = [MyPage, ResultsWaitPage, Results, FinalResults]
