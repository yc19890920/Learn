
class Player(object):

    def __init__(self, table, bet_strategy, game_strategy):
        self.table = table
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure( self.bet_strategy.bet() )

        # Yet more... Elided for now

"""
table = Table()
flat_bet = Flat()
dump = GameStrategy()
p = Player(table, flat_bet, dump)
p.game()
"""
# 换来代码的简洁，牺牲了大量的可读性，但易于扩展
# 这种基于关键字的初始化都放在基类，以简化子类
# 弊端：不易于维护
class Player2(object):

    def __init__(self, **kwargs):
        """ Must provided table, bet_strategy, game_strategy.
        """
        self.__dict__.update(kwargs)

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure( self.bet_strategy.bet() )

        # Yet more... Elided for now

"""
table = Table()
flat_bet = Flat()
dump = GameStrategy()
p = Player2(table=table, bet_strategy=flat_bet, game_strategy=dump)
p.game()
"""

class Player3(object):

    def __init__(self, table, bet_strategy, game_strategy, **extras):
        """ Must provided table, bet_strategy, game_strategy.
        """
        self.table = table
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.__dict__.update(extras)

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure( self.bet_strategy.bet() )

        # Yet more... Elided for now