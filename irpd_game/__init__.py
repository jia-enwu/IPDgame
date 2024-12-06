from otree.api import *

doc = """
Imagine you are a student representative and your goal is to collaborate with the university board to plan the usage of a new student building. Participating in the discussions ensures that students' voices are heard, and that the building design meets their needs. However, there is a risk that the university may not take your input seriously (i.e., the other party defects) and may use your attendance only to legitimize their decision-making process. This could harm your reputation and fail to serve the interests of the students. On the other hand, if you choose not to participate in the discussion (i.e., you defect), the resulting building design may not align with students' needs, but you will avoid potential negative consequences.

The costs and benefits of joining or not joining the cooperation meeting are represented in the payoff matrix below.

Payoff Matrix:

- If both you and the university cooperate (C, C), both parties benefit equally with a payoff of 35.
- If you cooperate but the university defects (C, D), you receive a payoff of 15, reflecting harm to your reputation and student interests.
- If you defect while the university cooperates (D, C), you receive a payoff of 40, representing a personal gain.
- If both defect (D, D), neither gains much, resulting in a payoff of 25 for both, which reflects a neutral outcome.

Please consider these payoffs carefully before making your decision.
"""


class C(BaseConstants):
    NAME_IN_URL = 'irpd_game'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 20
    PayoffCC = 35
    PayoffCD = 15
    PayoffDC = 40
    PayoffDD = 25
    StopProbability = 40  # 40% chance to stop after each round

class Subsession(BaseSubsession):
    pass

class Player(BasePlayer):
    decision = models.StringField(
        choices=['C', 'D'],
        widget=widgets.RadioSelect
    )

class Group(BaseGroup):
    stopped_early = models.BooleanField(initial=False)
    number = models.IntegerField()

    def set_payoffs(self):
        team1 = self.get_players()[:2]
        team2 = self.get_players()[2:]

        team1_decision = 'C' if all(p.decision == 'C' for p in team1) else 'D'
        team2_decision = 'C' if all(p.decision == 'C' for p in team2) else 'D'

        if team1_decision == 'C' and team2_decision == 'C':
            for p in team1 + team2:
                p.payoff = C.PayoffCC
        elif team1_decision == 'C' and team2_decision == 'D':
            for p in team1:
                p.payoff = C.PayoffCD
            for p in team2:
                p.payoff = C.PayoffDC
        elif team1_decision == 'D' and team2_decision == 'C':
            for p in team1:
                p.payoff = C.PayoffDC
            for p in team2:
                p.payoff = C.PayoffCD
        else:  # D, D
            for p in team1 + team2:
                p.payoff = C.PayoffDD

# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['decision']
    
    @staticmethod
    def vars_for_template(player: Player):
        instructions = """
            Imagine you are a student representative and your goal is to collaborate with the university board to plan the usage of a new student building. Participating in the discussions ensures that students' voices are heard, and that the building design meets their needs. However, there is a risk that the university may not take your input seriously (i.e., the other party defects) and may use your attendance only to legitimize their decision-making process. This could harm your reputation and fail to serve the interests of the students. On the other hand, if you choose not to participate in the discussion (i.e., you defect), the resulting building design may not align with students' needs, but you will avoid potential negative consequences.

            The costs and benefits of joining or not joining the cooperation meeting are represented in the payoff matrix below:

            - If both you and the university cooperate (C, C), both parties benefit equally with a payoff of 35.
            - If you cooperate but the university defects (C, D), you receive a payoff of 15, reflecting harm to your reputation and student interests.
            - If you defect while the university cooperates (D, C), you receive a payoff of 40, representing a personal gain.
            - If both defect (D, D), neither gains much, resulting in a payoff of 25 for both, which reflects a neutral outcome.
        """
        return {
            'instructions': instructions
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.group.stopped_early == False

import random
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(group: Group):
        group.set_payoffs()
        group.number = random.randint(0, 100)

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        teammates = player.get_players()[:2] if player.id_in_group <= 2 else player.get_players()[2:]
        opponents = player.get_players()[2:] if player.id_in_group <= 2 else player.get_players()[:2]
        return {
            'my_decision': player.decision,
            'teammates_decision': [p.decision for p in teammates],
            'opponents_decision': [p.decision for p in opponents],
            'payoff': player.payoff,
        }

    @staticmethod
    def is_displayed(player: Player):
        return player.group.stopped_early == False

    def before_next_page(player, timeout_happened):
        if player.group.number < C.StopProbability or player.group.round_number == C.NUM_ROUNDS:
            player.group.stopped_early = True

class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.group.stopped_early == True

    @staticmethod
    def vars_for_template(player: Player):
        total_payoff = sum([p.payoff for p in player.in_all_rounds()])
        return {
            'total_payoff': total_payoff,
        }

page_sequence = [MyPage, ResultsWaitPage, Results, FinalResults]