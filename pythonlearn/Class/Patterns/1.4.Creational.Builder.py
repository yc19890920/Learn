# -*- coding: utf-8 -*-


# factory pattern
MINI14 = '1.4GHz Mac mini'


class AppleFactory(object):

    class MacMini14(object):
        def __init__(self):
            self.memory = 4  # in gigabytes
            self.hdd = 500  # in gigabytes
            self.gpu = 'Intel HD Graphics 5000'

        def __str__(self):
            info = ('Model: {}'.format(MINI14),
                    'Memory: {}GB'.format(self.memory),
                    'Hard Disk: {}GB'.format(self.hdd),
                    'Graphics Card: {}'.format(self.gpu))
            return '\n'.join(info)

    def build_computer(self, model):
        if model == MINI14:
            return self.MacMini14()
        else:
            print("I don't know how to build {}".format(model))


# 使用工厂
afac = AppleFactory()
mac_mini = afac.build_computer(MINI14)
print(mac_mini)

"""
当对象需要多个部分组合起来一步步创建，并且创建和表示分离的时候。
可以这么理解，你要买电脑，工厂模式直接返回一个你需要型号的电脑，但是构造模式允许你自定义电脑各种配置类型，组装完成后给你。
这个过程你可以传入builder从而自定义创建的方式。
"""

# builder模式
class Computer(object):
    def __init__(self, serial_number):
        self.serial = serial_number
        self.memory = None      # in gigabytes
        self.hdd = None         # in gigabytes
        self.gpu = None

    def __str__(self):
        info = ('Memory: {}GB'.format(self.memory),
                'Hard Disk: {}GB'.format(self.hdd),
                'Graphics Card: {}'.format(self.gpu))
        return '\n'.join(info)

# 2、ConcreteBuilder:实现Builder的接口以构造和装配该产品的各个部件，定义并明确它所创建的表示，并提供一个检索产品的接口，也就是返回产品类的方法。
class ComputerBuilder(object):
    def __init__(self):
        self.computer = Computer('AG23385193')

    def configure_memory(self, amount):
        self.computer.memory = amount

    def configure_hdd(self, amount):
        self.computer.hdd = amount

    def configure_gpu(self, gpu_model):
        self.computer.gpu = gpu_model

# 3、Director:构造一个使用Builer接口的对象，该对象中定义了建造对象的步骤顺序。
class HardwareEngineer(object):
    def __init__(self):
        self.builder = None

    def construct_computer(self, memory, hdd, gpu):
        self.builder = ComputerBuilder()
        [ step for step in (
            self.builder.configure_memory(memory),
            self.builder.configure_hdd(hdd),
            self.builder.configure_gpu(gpu)
        )]

    @property
    def computer(self):
        return self.builder.computer

# 使用buidler，可以创建多个builder类实现不同的组装方式
engineer = HardwareEngineer()
engineer.construct_computer(hdd=500, memory=8, gpu='GeForce GTX 650 Ti')
computer = engineer.computer
print(computer)

