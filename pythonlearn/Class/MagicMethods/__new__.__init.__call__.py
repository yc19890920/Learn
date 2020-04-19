# -*- coding:utf-8 -*-

##############################################################################
class Singleton(object):

    a = 1
    b = 3

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.instance

obj1 = Singleton()
obj2 = Singleton()

print obj1.a == obj2.a
# True
obj1.a = 100
print obj2.a
# 100

obj1.attr1 = 'value1'
print obj1.attr1, obj2.attr1
# value1 value1
print obj1 is obj2
# True

##############################################################################
class Singleton2(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton2, cls).__new__(cls, *args, **kw)
        return cls._instance

class MyClass(Singleton2):
    a = 1

one = MyClass()
two = MyClass()
print one == two

##############################################################################
class Factorial(object):
    def __init__(self):
        self.cache = {}

    def __call__(self, n):
        # if n > 5:
        #     raise ValueError('n must be less than 5!')
        if n not in self.cache:
            if n == 0:
                self.cache[n] = 1
            else:
                self.cache[n] = n * self.__call__(n-1)
        return self.cache[n]


fact = Factorial()

for i in xrange(10):
    print("{}! = {}".format(i, fact(i)))

##############################################################################
class MakeTag(object):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            return "<{tag}>{res}</{tag}>".format(
                res=func(*args, **kwargs), tag=self.tag
            )
        return wrapped

@MakeTag(tag='p')
@MakeTag(tag='b')
def hello(name):
    return 'hello %s' % name

print hello('world')
# <p><b>hello world</b></p>


##############################################################################
import hashlib

class Hasher(object):
    """
     A wrapper around the hashlib hash algorithms that allows an entire file to
     be hashed in a chunked manner.
    """
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def __call__(self, file):
        hash = self.algorithm()
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), ''):
                hash.update(chunk)
        return hash.hexdigest()


md5 = Hasher(hashlib.md5)
sha1 = Hasher(hashlib.sha1)
sha224 = Hasher(hashlib.sha224)
sha256 = Hasher(hashlib.sha256)
sha384 = Hasher(hashlib.sha384)
sha512 = Hasher(hashlib.sha512)

print sha1('poetry.txt')


##############################################################################
class Animal(object):
    def __init__(self, name, legs):
        self.name = name
        self.legs = legs
        self.stomach = []

    def __call__(self,food):
        self.stomach.append(food)

    def poop(self):
        if len(self.stomach) > 0:
            return self.stomach.pop(0)

    def __str__(self):
        return 'A animal named %s' % (self.name)

cow = Animal('king', 4)  #We make a cow
dog = Animal('flopp', 4) #We can make many animals
print 'We have 2 animales a cow name %s and dog named %s,both have %s legs' % (cow.name, dog.name, cow.legs)
print cow  #here __str__ metod work

#We give food to cow
cow('gras')
print cow.stomach
# ['gras']

#We give food to dog
dog('bone')
dog('beef')
print dog.stomach
# ['bone', 'beef']

#What comes inn most come out
print cow.poop()
print cow.stomach  #Empty stomach

'''-->output
We have 2 animales a cow name king and dog named flopp,both have 4 legs
A animal named king
['gras']
['bone', 'beef']
gras
[]
'''