
class GameStrategy(object):

    def insurance(self, hand):
        return False

    def split(self, hand):
        return False

    def double(self, hand):
        return False

    def hit(self, hand):
        return sum(c.hard for c in hand.cards)<=17



