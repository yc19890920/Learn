# -*- coding: utf-8 -*-

class Newcar(object):
    '''Abstract Product'''
    def drive(self):
        pass

class NewBMW(Newcar):
    '''Concrete Product'''
    def __init__(self,carname):
        self.__name=carname
    def drive(self):
        print "Drive the New BMW as "+self.__name

class NewBenz(Newcar):
    '''Concrete Product'''
    def __init__(self,carname):
        self.__name=carname
    def drive(self):
        print "Drive the New Benz as "+self.__name

####################################
class Oldcar(object):
    '''Abstract Product'''
    def drive(self):
        pass

class OldBMW(Oldcar):
    '''Concrete Product'''
    def __init__(self,carname):
        self.__name=carname
    def drive(self):
        print "Drive the Old BMW as "+self.__name

class OldBenz(Oldcar):
    '''Concrete Product'''
    def __init__(self,carname):
        self.__name=carname
    def drive(self):
        print "Drive the Old Benz as "+self.__name

####################################
class Driver(object):
    '''Abstract Factory also called Creator'''
    def driverNewCar(self):
        return Newcar()
    def driverOldCar(self):
        return Oldcar()

class BMWdriver(Driver):
    '''Concrete Factory or Creator'''
    def driverNewCar(self):
        return NewBMW("NewBMW")
    def driverOldCar(self):
        return OldBMW("OldBMW")

class Benzdriver(Driver):
    '''Concrete Factory or Creator'''
    def driverNewCar(self):
        return NewBenz("NewBenz")
    def driverOldCar(self):
        return OldBenz("OldBenz")

if __name__ == "__main__":
    driver=BMWdriver()
    car=driver.driverNewCar()
    car.drive()

    car=driver.driverOldCar()
    car.drive()

    ####################################
    driver=Benzdriver()
    car=driver.driverNewCar()
    car.drive()

    car=driver.driverOldCar()
    car.drive()