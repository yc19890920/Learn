""" 模拟器
职责：
1. 玩家必须基于玩牌策略初始化一个牌局
2. 随后玩家会得到一手牌
3. 如果手中的牌是可以拆分的，玩家需要在基于当前玩法的情况下决定是否分牌。这会创建新的Hand对象，。在一些场合中，新分出去的牌是可以再分的。
4. 对于每个hand实例，玩家必须基于当前玩法决定叫牌、双倍还是停叫
5. 然后玩家会受到账单，他们可以根据输赢情况来决定之后的游戏策略。

基于以上，api函数 获取牌局、创建Hand对象、分牌、提供单手和多手策略以及支付。
这个对象的职责很多，用于追踪与Players集合所有相关操作的状态。
"""
from decker import Deck, Deck2, Deck3
from hander import Hand, Hand2

class Table(object):

    def __init__(self):
        self.deck = Deck3()

    def place_bet(self, amount):
        print("Bet", amount)

    def get_hand(self):
        try:
            self.hand = Hand2(self.deck.pop(), self.deck.pop(), self.deck.pop())
            self.hole_card = self.deck.pop()
        except IndexError as e:
            self.deck = Deck3()
            return self.get_hand()
        print("Deal", self.hand)
        return self.hand

    def can_insure(self, hand):
        return hand.dealer_card.insure


class BettingStrategy(object):

    def bet(self):
        raise NotImplementedError("No bet method")

    def record_win(self):
        pass

    def record_loss(self):
        pass

class Flat(BettingStrategy):

    def bet(self):
        return 1

import abc
class BettingStrategy2(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def bet(self):
        return 1

    def record_win(self):
        pass

    def record_loss(self):
        pass
