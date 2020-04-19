# -*- coding: utf-8 -*-

class car(object):
    '''interface as Product'''
    def drive(self):
        pass

class BMW(car):
    '''Concrete Product'''
    def __init__(self,carname):
        self.__name=carname
    def drive(self):
        print "Drive the BMW as "+self.__name

class Benz(car):
    '''Concrete Product'''
    def __init__(self,carname):
        self.__name=carname
    def drive(self):
        print "Drive the Benz as "+self.__name

class driver(object):
    '''Factory also called Creator'''
    def driverCar(self,name):
        if name=="BMW":
            return BMW("BMW")
        elif name=="Benz":
            return Benz("Benz")
        else:
            raise MyInputException(name)

class MyInputException(Exception):
    def __init__(self, name):
        Exception.__init__(self)
        self.name = name


# if __name__ == "__main__":
#     print "please input \"BMW\" or \"Benz\" :"
#     carname=raw_input()
#     dier=driver()
#     try:
#         d=dier.driverCar(carname)
#     except MyInputException,e:
#         print "input worry name "+e.name
#     else:
#         d.drive()


'''Factory also called Creator'''
def driver(name):
    if name=="BMW":
        return BMW("BMW")
    elif name=="Benz":
        return Benz("Benz")
    else:
        raise MyInputException(name)

if __name__ == "__main__":
    print "please input \"BMW\" or \"Benz\" :"
    carname=raw_input()
    try:
        d=driver(carname)
    except MyInputException,e:
        print "input worry name "+e.name
    else:
        d.drive()