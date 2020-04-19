# -*- coding: utf-8 -*-

# 主题/观察者模式

# 抽象的通知者(主题,发布者)
class Informer(object):
    observers = []
    action = ''

    def Attach(self, observer):
        self.observers.append(observer)

    def Notify(self):
        for o in self.observers:
            o.Update()

# 秘书(主题1)
class Secretary(Informer):
    observers = []
    action = u"老板回来了!"


# 老板(主题2)
class Boss(Informer):
    observers = []
    update = [] # 更新函数接口列表
    action = u"我胡汉三回来了!"

    def AddEventCB(self,eventCB):
        self.update.append(eventCB)

    def Notify(self):
        for o in self.update:
            o()


# 抽象的观察者
class Observer(object):
    name = ''
    nformer = None;

    def __init__(self, name, secretary):
        self.name = name
        self.secretary = secretary # secretary是观察者要订阅的主题

    def Update(self):
        pass

# 看股票的同事(观察者1)
class StockObserver(Observer):
    name = ''
    secretary = None;

    def __init__(self, name, secretary):
        Observer.__init__(self, name, secretary)

    def Update(self):
        print(u"%s %s, 不要看股票了，继续工作" % (self.secretary.action,self.name))

    def CloseStock(self):
        print(u"%s %s, 不要看股票了，TMD快点工作!!!" % (self.secretary.action,self.name))

# 看NBA的同事(观察者2)
class NBAObserver(Observer):
    name = ''
    secretary = None;

    def __init__(self, name, secretary):
        Observer.__init__(self, name, secretary)

    def Update(self):
        print(u"%s %s, 不要看NBA了，继续工作" % (self.secretary.action,self.name))

def clientUI():
    # 传递对象实现
    secretary = Secretary()
    stockObserver1 = StockObserver(u'张三', secretary)
    nbaObserver1 = NBAObserver(u'王五', secretary)

    secretary.Attach(stockObserver1)
    secretary.Attach(nbaObserver1)

    secretary.Notify()

    # 回调函数实现
    huHanShan = Boss()
    stockObserver2 = StockObserver(u'李四', huHanShan)
    huHanShan.AddEventCB(stockObserver2.CloseStock)
    huHanShan.Notify()
    return


if __name__ == '__main__':
    clientUI()

# 观察者订阅一个主题(把自己的回调函数/对象传递给主题),主题调用观察者的方法来通知观察者的