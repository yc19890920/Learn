# -*- coding: utf-8 -*-

class Hero(object):

    def say_self_hello(self, value):
        print("Helllo self..., then %"% value)

    @staticmethod
    def say_hello(name):
        print("Hi %s..." % name)

    @staticmethod
    def say_son(name):
        pass

    @classmethod
    def say_class_hello(cls):
        if(cls.__name__=="HeroSon"):
            # print "Hi Kido"
            cls.say_son("Kido")
        elif(cls.__name__=="HeroDaughter"):
            # print("Hi Princess")
            cls.say_hello("Princess")

class HeroSon(Hero):
    def say_son_hello(self):
        print("test  hello")

    @staticmethod
    def say_son(name):
        print("Helllo son(%s)..." % name)


class HeroDaughter(Hero):
    def say_daughter_hello(self):
        print("test  hello daughter")




testSon = HeroSon()

testSon.say_class_hello()
# Output: Helllo son(Kido)...

testSon.say_hello('son')
# Outputs: Hi son...

testDaughter = HeroDaughter()

testDaughter.say_class_hello()
# Outputs: Hi Princess...

testDaughter.say_hello('girl')
# Outputs: Hi girl...



