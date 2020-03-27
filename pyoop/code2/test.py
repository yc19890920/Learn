
from carder import AceCard
from decker import Deck, Deck2, Deck3
from hander import LazyHand

c1 = AceCard(1, "♣")
c2 = AceCard(1, "♣")

print(c1, c2, id(c1), id(c2))

d = Deck()
h = LazyHand(d.pop(), d.pop(), d.pop())
print(h.total)
h.card = d.pop()
print(h.total)



