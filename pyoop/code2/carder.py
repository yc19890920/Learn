""" 多态
子类重用基类的实现
"""

class Card(object):

    insure =  False

    def __init__(self, rank, suit, hard, soft):
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self):
        return "{__class__.__name__}({rank!r}, {suit!r})".format(
            __class__=self.__class__,
            **self.__dict__
        )

    def __str__(self):
        return  "{rank}{suit}".format(**self.__dict__)

    def __eq__(self, other):
        return self.rank==other.rank and self.suit==other.suit

    # def __hash__(self):
    #     """ 通过两个基本数字的所有位异或计算一种新的位模式。
    #     :return:
    #     """
    #     return self.rank ^ self.suit

    __hash__ = None


class NumberCard(Card):

    insure =  True

    def __init__(self, rank, suit):
        super(NumberCard, self).__init__(str(rank), suit, rank, rank)
        # super().__init__(str(rank), suit, rank, rank)

class AceCard(Card):

    insure =  True

    def __init__(self, rank, suit):
        super().__init__("A", suit, 1, 11)

class FaceCard(Card):

    insure =  True

    def __init__(self, rank, suit):
        super().__init__({11:"J", 12: "Q", 13: "K"}[rank], suit, 10, 10)


# c1 = AceCard(1, "♣")
# c2 = AceCard(1, "♣")
# print(hash(c1), hash(c2))
# print(id(c1), id(c2))
# print(c1==c2)

def card1(rank, suit):
    if rank==1: return AceCard('A', suit)
    elif 2<=rank<11: return NumberCard(str(rank), suit)
    elif 11<=rank<14:
        return FaceCard({11:"J", 12: "Q", 13: "K"}[rank], suit)
    else:
        raise Exception("Rank out of range")

# 2. 元组
def card5(rank, suit):
    class_, rank_ = {
        1: (AceCard, "A"),
        11: (FaceCard, "J"),
        12: (FaceCard, "Q"),
        13: (FaceCard, "K"),
    }.get(rank, (NumberCard, str(rank)))
    return class_(rank_, suit)

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

    def suit(self, rank, suit):
        return self.class_(rank, suit)

card7 = CardFactory()