from otree.api import *


doc = """
This is an iterative "Prisoner's Dilemma" game. Two players are asked separately
whether they want to cooperate or defect. The game continues with a probability of 3/4 after each round.
Their choices directly determine the payoffs.
"""


class C(BaseConstants):
    NAME_IN_URL = 'irpd_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 20
    PayoffCC = 35
    PayoffCD = 15
    PayoffDC = 40
    PayoffDD = 25
    StopProbability = 50  # 50% chance to stop after each round

class Subsession(BaseSubsession):
    pass

class Player(BasePlayer):
    decision = models.StringField(
        choices=[
            ('C', 'Cooperate with the university'),
            ('D', 'Refuse to cooperate with the university')
        ],
        widget=widgets.RadioSelect
    )

class Group(BaseGroup):
    stopped_early = models.BooleanField(initial=False)
    number = models.IntegerField()

# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['decision']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.stopped_early == False

import random
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(group: Group):
        p1 = group.get_players()[0]
        p2 = group.get_players()[1]

        if p1.decision == 'C' and p2.decision == 'C':
            p1.payoff = C.PayoffCC
            p2.payoff = C.PayoffCC
        if p1.decision == 'C' and p2.decision == 'D':
            p1.payoff = C.PayoffCD
            p2.payoff = C.PayoffDC
        if p1.decision == 'D' and p2.decision == 'C':
            p1.payoff = C.PayoffDC
            p2.payoff = C.PayoffCD
        if p1.decision == 'D' and p2.decision == 'D':
            p1.payoff = C.PayoffDD
            p2.payoff = C.PayoffDD

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




