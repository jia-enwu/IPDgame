from otree.api import *

doc = """
Game 1: This game introduces participants to either the treatment or control group, with consistent pairing within groups. Participants also receive different instructions in the introduction based on their introduction group.
"""

import random

class C(BaseConstants):
    NAME_IN_URL = 'irpd_game_1'
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
        # Track counts to balance between treatment and control
        treatment_count = 0
        control_count = 0

        for player in self.get_players():
            # Assign treatment/control group in a balanced way
            if treatment_count <= control_count:
                player.participant.vars['treatment'] = 'treatment'
                treatment_count += 1
            else:
                player.participant.vars['treatment'] = 'control'
                control_count += 1

            # Assign introduction treatment/control group
            player.participant.vars['intro_treatment'] = random.choice(['intro_treatment', 'intro_control'])

            # Logging assignments for debugging
            print(f"Participant {player.id_in_group} assigned to treatment group: {player.participant.vars['treatment']}")
            print(f"Participant {player.id_in_group} assigned to intro group: {player.participant.vars['intro_treatment']}")


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
        # Assign default treatment if missing; should not happen if creating_session() works properly
        if 'treatment' not in self.participant.vars:
            self.participant.vars['treatment'] = 'control'
            print(f"Warning: treatment assignment was missing for participant {self.id_in_group}, assigning 'control'.")
        return self.participant.vars['treatment']

    @property
    def intro_treatment(self):
        # Assign default intro_treatment if missing; should not happen if creating_session() works properly
        if 'intro_treatment' not in self.participant.vars:
            self.participant.vars['intro_treatment'] = random.choice(['intro_treatment', 'intro_control'])
            print(f"Warning: intro_treatment assignment was missing for participant {self.id_in_group}, assigning randomly.")
        return self.participant.vars['intro_treatment']


class Group(BaseGroup):
    stopped_early = models.BooleanField(initial=False)
    number = models.IntegerField()


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        # Display Introduction page only in the first round
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        # Use the introduction group variable assigned during creating_session()
        return {
            'intro_group': player.intro_treatment
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Ensure intro_treatment and treatment are assigned before proceeding
        if 'intro_treatment' not in player.participant.vars:
            player.participant.vars['intro_treatment'] = random.choice(['intro_treatment', 'intro_control'])
            print(f"Warning: intro_treatment was missing for participant {player.id_in_group}, assigning randomly.")
        if 'treatment' not in player.participant.vars:
            player.participant.vars['treatment'] = 'control'
            print(f"Warning: treatment was missing for participant {player.id_in_group}, assigning 'control'.")


class MyPage(Page):
    form_model = 'player'
    form_fields = ['decision']

    @staticmethod
    def is_displayed(player: Player):
        # Display MyPage only if the game has not stopped early
        return not player.group.stopped_early

    @staticmethod
    def vars_for_template(player: Player):
        # Ensure treatment is assigned before using it
        if 'treatment' not in player.participant.vars:
            player.participant.vars['treatment'] = 'control'
            print(f"Warning: treatment was missing for participant {player.id_in_group}, assigning 'control'.")

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


# Update the page sequence to include Introduction first
page_sequence = [Introduction, MyPage, ResultsWaitPage, Results, FinalResults]
