# -*- coding: utf-8 -*-

a = '{1:.2f}{0}'.format('a', 3.1415926)

args=['lu']
kwargs = {'name1': 'Kevin', 'name2': 'Tom'}
print 'hello {name1} {} i am {name2}'.format(*args, **kwargs)  # hello Kevin i am Tom

print '{{ hello {0} }}'.format('Kevin')

print 'hello {0:>{1}} '.format('Kevin',50)

from string import Template
print Template('$name $age').substitute({'name':'admin'}, age=22)
print Template('$name $age').safe_substitute({'name':'admin'})
print Template('$name $age $$').safe_substitute({'name':'admin'})

import re

def safe_format(template, **kwargs):
    def replace(mo):
        name = mo.group('name')
        if name in kwargs:
            return unicode(kwargs[name])
        else:
            return mo.group()

    p = r'\{(?P<name>\w+)\}'
    return re.sub(p, replace, template)

if __name__ == "__main__":
    import datetime
    kwargs = {}
    kwargs.update(
        COMPANY=u'深圳市XXXX科技有限公司', NAME=u'Allen',
        TIME=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), AREA=u'深圳福田',
        POINT=100, DOMAIN=u'test.com',
    )
    template = u'尊敬的{COMPANY}-{NO_REPLACE} ，贵司账号在{AREA}登陆XXXX营销系统，如果不是授权行为，请及时修改密码和检查微信绑定账号！'
    template = safe_format(template, **kwargs)
    print template
