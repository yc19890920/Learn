""" 封装集合类
"""

import random
from carder import card7
from suiter import Club, Diamond, Heart, Spade

# 1. 封装 外观模式。
class Deck(object):

    def __init__(self):
        self._cards = [card7.rank(r+1).suit(r+1, s) for r in range(13) for s in (Club, Diamond, Heart, Spade)]
        random.shuffle(self._cards)

    def pop(self):
        return self._cards.pop()

    def __bool__(self):
        return bool(self._cards)


# 2. 扩展集合类
class Deck2(list):

    def __init__(self):
        super().__init__(
            card7.rank(r+1).suit(s) for r in range(13) for s in (Club, Diamond, Heart, Spade)
        )
        random.shuffle(self)

    def __bool__(self):
        return bool(self._cards)

# 适应更多需求的类
class Deck3(list):

    def __init__(self, decks=1):
        super().__init__() # 构建空集合
        for i in range(decks): # 多副牌加载到发牌机中。
            self.extend(
                card7.rank(r+1).suit(s) for r in range(13) for s in (Club, Diamond, Heart, Spade)
            )
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()

    def __bool__(self):
        """ 返回真假，确认有没有卡牌
        :return:
        """
        return bool(self._cards)