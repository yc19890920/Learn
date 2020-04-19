# -*- coding: utf-8 -*-
#

import re

# 匹配邮箱
RE_COMPILE_MAIL = re.compile(
    '^(\w|[-+=.])+@\w+([-.]\w+)*\.(\w+)$'
)

# 匹配手机
RE_COMPILE_PHONE = re.compile(
    r'((\+?86)|(\(\+86\)))?(\s)?(13[012356789][0-9]{8}|15[012356789][0-9]{8}|18[02356789][0-9]{8}|14[57][0-9]{8}|1349[0-9]{7}|177[0-9]{8})'
)

# 匹配IP地址
RE_COMPILE_IPADDR = re.compile(
    '(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)'
)

# 字符串替换
def safe_format(template, **kwargs):
    def replace(mo):
        name = mo.group('name')
        if name in kwargs:
            return unicode(kwargs[name])
        else:
            return mo.group()

    p = r'\{(?P<name>\w+)\}'
    return re.sub(p, replace, template)


#############################################
### html内容删除外部资源（css、js） ###
def remove_js_and_css(html):
    html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
    # html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
    html = re.sub(r'<link .*?>', '', html, flags=re.DOTALL|re.IGNORECASE)
    return html

def html_add_footer(html, footer):
    m = re.search(r'</\s*(body|html)>', html, re.IGNORECASE)
    if m is not None:
        s = m.start()
    else:
        s = len(html)
    return html[:s] + footer + html[s:]


if __name__ == "__main__":
    import datetime
    kwargs = {}
    kwargs.update(
        COMPANY=u'深圳市XXXX科技有限公司', NAME=u'Allen',
        TIME=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), AREA=u'深圳福田',
        POINT=100, DOMAIN=u'test.com',
        TASK='', LAVE='',
    )
    template = u'尊敬的{COMPANY} ，贵司账号在{AREA}登陆XXXX营销系统，如果不是授权行为，请及时修改密码和检查微信绑定账号！\n有任何疑问请致电400-XXXX-XXX，我们将竭诚为您服务！'
    template = safe_format(template, **kwargs)
    print template

