
class Hand6(object):

    def __str__(self):
        return ", ".join(map(str, self.card))

    def __repr__(self):
        return "{__class__.__name__}({dealer_card!r}, {_cards_str!r})".format(
            __class__=self.__class__,
            _cards_str=", ".join(map(repr, self.card)),
            **self.__dict__
        )

    def __eq__(self, other):
        return self.card==other.card and self.dealer_card==other.dealer_card

    __hash__ = None

class LazyHand(Hand6):

    def __init__(self, dealer_card, *cards):
        self.dealer_card = dealer_card
        self._cards = list(cards)

    @property
    def total(self):
        delta_soft = max(c.soft-c.hard for c in self._cards)
        hard_soft = sum(c.hard for c in self._cards)
        if hard_soft+delta_soft<=21:return hard_soft+delta_soft
        return hard_soft

    @property
    def card(self):
        return self._cards

    @card.setter
    def card(self, setCard):
        self._cards.append(setCard)

    @card.deleter
    def card(self):
        self._cards.pop()


class EagerHand(Hand6):

    def __init__(self, dealer_card, *cards):
        self.dealer_card = dealer_card
        self._cards = list(cards)
        self.total = 0
        self._delta_soft=0
        self._hard_soft=0
        self._cards = list()
        for c in cards:
            self.card = c

    @property
    def card(self):
        return self._cards

    @card.setter
    def card(self, setCard):
        self._cards.append(setCard)
        self._delta_soft = max(setCard.soft-setCard.hard, self._delta_soft)
        self._hard_soft += setCard.hard
        self._set_total()

    @card.deleter
    def card(self):
        removed = self._cards.pop(-1)
        self._hard_soft -= removed.hard
        self._delta_soft = max(c.soft-c.hard for c in self._cards)
        self._set_total()

    def _set_total(self):
        if self._hard_soft+self._delta_soft<=21:
            self.total = self._hard_soft+self._delta_soft
        else:
            self.total = self._hard_soft