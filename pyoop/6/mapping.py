import collections.abc
import shelve
import math
from collections import Counter

class StatsContainer(Counter):

    @property
    def mean(self):
        sum0 = sum(v for _, v in self.items())
        sum1 = sum(k*v for k,v in self.items())
        return sum1/sum0

    @property
    def mean(self):
        sum0 = sum(v for _, v in self.items())
        sum1 = sum(k*v for k,v in self.items())
        sum2 = sum(k*k*v for k,v in self.items())
        return ( sum1 and math.sqrt(sum0*sum2 - sum1*sum1)/sum1 or 0 )