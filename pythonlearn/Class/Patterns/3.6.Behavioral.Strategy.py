# -*- coding: utf-8 -*-
#

class Duck(object):
    # 上面使用继承，这里通用的使用参数方式，传入的就是操作工厂的类
    def __init__(self, strategy=None):
        self.action = None
        self.count = 0
        if strategy:
            # 指定策略，那么执行action就是用这个类的实例
            self.action = strategy()

    def fly(self, kind):
        if self.action:
            self.count += 1
            # 这里的第二个参数self，算是炫技吧，就是为了让操作的方法获得这里计算好的count
            return self.action.fly(kind, self)
        else:
            raise UnboundLocalError('Exception raised, no strategyClass supplied to Duck!')

# 注意这里没有继承Duck，因为是以参数的方式传入类名
class Duck1(object):

    def fly(self, kind, instance):
        return 'Duck1 fly kind: ' + kind + '#' + str(instance.count)


class Duck2(object):

    def fly(self, kind, instance):
        return 'Duck2 fly kind: ' + kind + '#' + str(instance.count)


if __name__ == '__main__':
    duckfly = Duck()
    duck1fly = Duck(strategy=Duck1)
    duck2fly = Duck(strategy=Duck2)

    try:
        print duckfly.fly('yes')
    except Exception as e:
        print "The following exception was expected:"
        print e

    print duck1fly.fly('yes')
    print duck1fly.fly('no')
    print duck1fly.fly('yes')
    print duck2fly.fly('yes')
    print duck2fly.fly('no')