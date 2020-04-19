# -*- coding: utf-8 -*-



import json
import xml.etree.ElementTree as etree

class JSONConnector(object):
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r') as f:
            self.data = json.load(f)

    @property
    def parsed_data(self):
        return self.data


class XMLConnector(object):
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        return self.tree


def connection_factory(filepath):
    """ 工厂方法 """
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector(filepath)





#
# if __name__ == "__main__":
#     jsonPs = connection_factory('hello.json')
#     print jsonPs.parsed_data
#
#
#     xmlPs = connection_factory('hello.xml')
#     for x in  xmlPs.parsed_data.iter():
#          # 'append', 'attrib', 'clear', 'copy', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'insert', 'items', 'iter', 'iterfind', 'itertext', 'keys', 'makeelement', 'remove', 'set', 'tag', 'tail', 'text'
#         print x.text

###########################################################

class Pizza(object):
  def prepare(self):
    print 'prepare pizza'

  def bake(self):
    print 'bake pizza'

  def cut(self):
    print 'cut pizza'

  def box(self):
    print 'box pizza'


class GZCheesePizza(Pizza):
  def __init__(self):
    self.name = "guangzhou cheese pizza"


class GZClamPizza(Pizza):
  def __init__(self):
    self.name = "guangzhou clam pizza"


class GZVeggiePizza(Pizza):
  def __init__(self):
    self.name = "guangzhou veggie pizza"


class PizzaStore(object):
  def create_pizza(self, item):
    raise NotImplementedError

  def order_pizza(self, type):
    pizza = self.create_pizza(type)
    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()
    return pizza


class GZPizzaStore(PizzaStore):
  def create_pizza(self, type):
    pizza = None

    if type == "cheese":
      pizza = GZCheesePizza()
    elif type == "clam":
      pizza = GZClamPizza()
    elif type == "veggie":
      pizza = GZVeggiePizza()

    return pizza


if __name__ == "__main__":
  gz_store = GZPizzaStore()
  pizza = gz_store.order_pizza('cheese')
  print pizza.name
