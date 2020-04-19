# -*- coding: utf-8 -*-
#

from collections import namedtuple


BaseFormFieldFormat = lambda field_names: namedtuple("BaseFormFieldFormat", field_names)
BaseFieldFormat = BaseFormFieldFormat(['value', 'error'])
BaseFieldFormatExt = BaseFormFieldFormat(['value', 'error', 'extra'])
BaseFieldFormatOption = BaseFormFieldFormat(['type', 'action', 'value', 'error' ])

class AForm(object):

    class FieldList(object):
        name = None
        option = None
        sequence = None

    name = property(fget=lambda self: self.__form.name, fset=None, fdel=None, doc=None)
    option = property(fget=lambda self: self.__form.option, fset=None, fdel=None, doc=None)
    sequence = property(fget=lambda self: self.__form.sequence, fset=None, fdel=None, doc=None)

    def __init__(self):
        self.__valid = True
        self.__init()


    def __init(self):
        self.__form = AForm.FieldList()
        self.__form.name = BaseFieldFormat(value="", error=None)
        self.__form.option = BaseFieldFormatOption(type="subject", action="in", value="", error=None)
        self.__form.sequence = BaseFieldFormat(value=3, error=None)

    def is_valid(self):
        self.__check()
        return self.__valid

    def __check(self):
        if self.sequence.value >= 3:
            # 替换属性值
            self.__form.sequence = self.__form.sequence._replace(error=u'sequence can not gte 3!')
            self.__valid = False

    def scan(self):
        print self.name.value, '--', self.name.error
        print self.option.value, '--', self.option.error
        print self.sequence.value, '--', self.sequence.error


if __name__ == "__main__":
    form = AForm()

    if form.is_valid():
        pass

    form.scan()


