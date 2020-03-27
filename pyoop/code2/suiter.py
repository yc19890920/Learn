""" 创建花色
"""
class Suit(object):

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return "{__class__.__name__}({name!r}, {symbol!r})".format(
            __class__=self.__class__,
            name=self.name, symbol=self.symbol
        )

    def __str__(self):
        return "({name}{symbol})".format(**self.__dict__)

Club, Diamond, Heart, Spade = Suit("Club", "♣"), Suit("Diamond", "♦"), Suit("Heart", "♥"), Suit("Spade", "♠")

# print(Club, Diamond, Heart, Spade)
