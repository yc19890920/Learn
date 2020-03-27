"""  创建卡牌
"""

class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.hard, self.soft = self._points()


class NumberCard(Card):

    def _points(self):
        return int(self.rank), int(self.rank)

class AceCard(Card):

    def _points(self):
        return 1, 11

class FaceCard(Card):

    def _points(self):
        return 10, 10

class RankError(Exception):
    pass


def card1(rank, suit):
    if rank==1: return AceCard('A', suit)
    elif 2<=rank<11: return NumberCard(str(rank), suit)
    elif 11<=rank<14:
        return FaceCard({11:"J", 12: "Q", 13: "K"}[rank], suit)
    else:
        raise RankError("Rank out of range")

# 使用 映射来简化类
def card2(rank, suit):
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, NumberCard)
    return class_(rank, suit)


# 使用defaultdict
# defaultdict类的默认构造函数必须是无参的，使用一个lambda构造函数作为常量的封装函数
from collections import defaultdict
card3 = defaultdict(lambda: NumberCard, {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard} )



# 1. 并行映射
# 重复是糟糕的，映射键1， 11， 12， 13的逻辑重复，软件更新后通常会带来对并行结构多余的维护成本
def card4(rank, suit):
    class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, NumberCard)
    rank_ = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(rank, str(rank))
    return class_(rank_, suit)

# 2. 元组
def card5(rank, suit):
    class_, rank_ = {
        1: (AceCard, "A"),
        11: (FaceCard, "J"),
        12: (FaceCard, "Q"),
        13: (FaceCard, "K"),
    }.get(rank, (NumberCard, str(rank)))
    return class_(rank_, suit)

# 3. partial函数
from functools import partial
def card6(rank, suit):
    class_ = {
        1: partial(AceCard, "A"),
        11: partial(FaceCard, "J"),
        12: partial(FaceCard, "Q"),
        13: partial(FaceCard, "K"),
    }.get(rank, partial(NumberCard, str(rank)))
    return class_(suit)


# 4. 工程模式的流畅API设计
# 顺序调用
# 先使用rank()函数更新了构造函数的状态， 然后通过suit()函数创造了最终的Card对象
class CardFactory(object):

    def rank(self, rank):
        self.class_, self.rank_ = {
            1: (AceCard, "A"),
            11: (FaceCard, "J"),
            12: (FaceCard, "Q"),
            13: (FaceCard, "K"),
        }.get(rank, (NumberCard, str(rank)))
        return self

    def suit(self, suit):
        return self.class_(self.rank_, suit)

card7 = CardFactory()
