# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from enum import Enum

State = Enum('State', 'new running sleeping restart zombie')


class Server(object):
    """ 抽象基类 """
    __metaclass__ = ABCMeta
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self, restart=True):
        pass

#一个模块化的操作系统可以有很多服务进程：文件服务进程、进程服务进程等。
#文件服务进程
class FileServer(Server):
    def __init__(self):
        '''actions required for initializing the file server'''
        self.name = 'FileServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''actions required for booting the file server'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        '''actions required for killing the file server'''
        self.state = State.restart if restart else State.zombie

    #用于创建文件
    def create_file(self, user, name, permissions):
        '''check validity of permissions, user rights, etc.'''
        print("trying to create the file '{}' for user '{}' with permissions {}".format(name, user, permissions))

class ProcessServer(Server):
    def __init__(self):
        '''actions required for initializing the process server'''
        self.name = 'ProcessServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''actions required for booting the process server'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        '''actions required for killing the process server'''
        self.state = State.restart if restart else State.zombie

    #用于创建进程
    def create_process(self, user, name):
        '''check user rights, generate PID, etc.'''
        print("trying to create the process '{}' for user '{}'".format(name, user))

#进程服务进程
class OperatingSystem(object):
    ''' 实现外观模式，外部使用的代码不必知道 FileServer 和 ProcessServer的
    内部机制，只需要通过 OperatingSystem类调用'''
    def __init__(self): #__init__()方法中创建所有需要的服务进程
        self.fs = FileServer()
        self.ps = ProcessServer()

    def start(self):
        """ start()方法是系统的入口点，供客户端代码使用 """
        [i.boot() for i in (self.fs, self.ps)]

    def create_file(self, user, name, permissions):
        return self.fs.create_file(user, name, permissions)

    def create_process(self, user, name):
        return self.ps.create_process(user, name)

def main():
    os = OperatingSystem()
    os.start()
    os.create_file('foo', 'hello', '-rw-r-r')
    os.create_process('bar', 'ls /tmp')

if __name__ == "__main__":
    main()