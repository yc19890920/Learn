
class Hand(object):

    def __init__(self, dealer_card):
        self.dealer_card = dealer_card
        self.cards = []

    def hard_total(self):
        return sum(c.hard for c in self.cards)

    def soft_total(self):
        return sum(c.soft for c in self.cards)


class Hand2(object):

    def __init__(self, dealer_card, *cards):
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def hard_total(self):
        return sum(c.hard for c in self.cards)

    def soft_total(self):
        return sum(c.soft for c in self.cards)

    def __str__(self):
        return ", ".join(map(str, self.cards))

    def __repr__(self):
        return "{__class__.__name__}({dealer_card!r}, {_cards_str!r})".format(
            __class__=self.__class__,
            _cards_str=", ".join(map(repr, self.cards)),
            **self.__dict__
        )

    def __eq__(self, other):
        return self.cards==other.cards and self.dealer_card==other.dealer_card

    __hash__ = None


class Hand3(object):

    def __init__(self, *args, **kwargs):
        if len(args)==1 and isinstance(args[0], Hand3):
            # Clone an existing hand; often a bad idea
            other = args[0]
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        else:
            # Build a fresh, new hand.
            dealer_card, *cards = args
            self.dealer_card = dealer_card
            self.cards = list(cards)

    def hard_total(self):
        return sum(c.hard for c in self.cards)

    def soft_total(self):
        return sum(c.soft for c in self.cards)

class Hand4(object):

    def __init__(self, *args, **kwargs):
        if len(args)==1 and isinstance(args[0], Hand3):
            # Clone an existing hand; often a bad idea
            other = args[0]
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        elif len(args)==2 and isinstance(args[0], Hand3) and 'split' in kwargs:
            # Split an existing hand
            other, card = args
            self.dealer_card = other.dealer_card
            self.cards = [other.cards[kwargs['split']], card]
        elif len(args)==3:
            # Build a fresh, new hand.
            dealer_card, *cards = args
            self.dealer_card = dealer_card
            self.cards = list(cards)
        else:
            raise TypeError("Invalid constructor args={0!r} kwargs={1!r}".format(args, kwargs))

    def __str__(self):
        return ", ".join(map(str, self.cards))

    def __repr__(self):
        return "{__class__.__name__}({dealer_card!r}, {_cards_str!r})".format(
            __class__=self.__class__,
            _cards_str=", ".join(map(repr, self.cards)),
            **self.__dict__
        )

    def __eq__(self, other):
        return self.cards==other.cards and self.dealer_card==other.dealer_card

    __hash__ = None

class Hand5(object):

    def __init__(self, dealer_card, *cards):
        self.dealer_card = dealer_card
        self.cards = list(cards)

    @staticmethod
    def freeze(other):
        return Hand5(other.dealer_card, *other.cards)

    @staticmethod
    def split(other, card0, card1):
        return (
            Hand5(other.dealer_card, other.cards[0], card0),
            Hand5(other.dealer_card, other.cards[1], card1)
        )

    def __str__(self):
        return ", ".join(map(str, self.cards))

    def __repr__(self):
        return "{__class__.__name__}({dealer_card!r}, {_cards_str!r})".format(
            __class__=self.__class__,
            _cards_str=", ".join(map(repr, self.cards)),
            **self.__dict__
        )

    def __eq__(self, other):
        return self.cards==other.cards and self.dealer_card==other.dealer_card

    __hash__ = None

"""
d = Deck()
h = Hand5(d.pop, d.pop, d.pop)
s1, s2 = Hand5.split(h, d.pop, d.pop)
"""

import sys
class FrozenHand(Hand5):

    def __init__(self, *args, **kwargs):
        if len(args)==1 and isinstance(args[0], Hand5):
            # clone a hand
            other = args[0]
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        else:
            # Build a fresh, new hand.
            super().__init__(*args, **kwargs)

    def __hash__(self):
        h=0
        for c in self.cards:
            h = (h+hash(c))%sys.hash_info.modulus
        return h



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