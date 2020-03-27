
class BlackJackCard(object):
    """ Abstract SuperClass
    """

    __slots__ = ('rank', 'suit', 'hard', 'soft')

    def __init__(self, rank, suit, hard, soft):
        super().__setattr__('rank', rank)
        super().__setattr__('suit', suit)
        super().__setattr__('hard', hard)
        super().__setattr__('soft', soft)

    def __str__(self):
        return "{0.rank}{0.suit}".format(self)

    def __setattr__(self, key, value):
        raise AttributeError(
            "'{__class__.__name__}' has no attribute '{key}'".format(
             __class__=self.__class__, key=key))


class BlackJackCard2(tuple):

    def __new__(cls, rank, suit, hard, soft):
        return super().__new__(cls, (rank, suit, hard, soft))

    def __getattr__(self, item):
        return self[{'rank': 0, 'suit': 1, 'hard': 2, 'soft': 3}[item]]

    def __setattr__(self, key, value):
        # raise AttributeError
        raise AttributeError(
            "'{__class__.__name__}' has no attribute '{key}'".format(
             __class__=self.__class__, key=key))


d = BlackJackCard2("A", "梅花", 1, 11)
print(d, d.rank, d.suit)

print(d[1])

# d.rank = 123

print(d.__dict__)
d.__dict__["aa"] = 1
print(d.__dict__)
