""" 创建花色
"""
class Suit(object):

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

Club, Diamond, Heart, Spade = Suit("Club", "♣"), Suit("Diamond", "♦"), Suit("Heart", "♥"), Suit("Spade", "♠")
