
from suiter import Club, Diamond, Heart, Spade
from carder import NumberCard, AceCard, FaceCard
from carder import card7

cards = [ AceCard("A", Spade), NumberCard("2", Spade), NumberCard("3", Spade), FaceCard("J", Spade)]

deck8 = [card7.rank(r).suit(s) for r in range(13) for s in (Club, Diamond, Heart, Spade)]
print(deck8)
