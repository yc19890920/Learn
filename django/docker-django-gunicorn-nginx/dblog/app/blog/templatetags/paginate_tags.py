# -*- coding: utf-8 -*-
from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()
# 这是定义模板标签要用到的


@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    # context是Context 对象，object_list是你要分页的对象，page_count表示每页的数量
    left = 3
    right = 3
    # 获取分页对象
    # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
    # paginator 是 Paginator 的一个实例，
    # page_obj 是 Page 的一个实例，
    # is_paginated 是一个布尔变量，用于指示是否已分页。
    # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
    # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
    # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
    paginator = Paginator(object_list, page_count)
    # 从请求中获取页码号
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page) # 根据页码号获取数据页码对象
        # context['current_page'] = int(page) # 将当前页码号封装进context中
        current_page = int(page)
        # 获取页码列表
        pages = paginator.page_range

    except PageNotAnInteger:
        object_list = paginator.page(1) # 获取首页数据页码对象
        current_page = 1
        # context['current_page'] = 1
        pages = paginator.page_range

    except EmptyPage:
        # 用户传递的是一个空值，则把最后一页返回给他
        object_list = paginator.page(paginator.num_pages)
        # num_pages为总分页数
        context['currten_page'] = paginator.num_pages
        pages = paginator.page_range
    # 获得分页后的总页数
    num_pages = paginator.num_pages

    # 将 pages 修改为省略号（0代表省略）
    pages = get_pages(pages, current_page, num_pages)

    context['current_page'] = current_page
    context['article_list'] = object_list
    context['pages'] = pages  # 页码列表
    context['last_page'] = num_pages
    context['first_page'] = 1
    # 用于判断是否加入省略号
    try:
        context['page_first'] = pages[0]
        context['page_last'] = pages[-1] + 1
    except IndexError:
        context['page_first'] = 1
        context['page_last'] = 2
    return ''

def get_pages(page_xrange, current_page, page_all):
    """get the paginator"""
    page_range = []
    mid_pages = 3  # 中间段显示的页码数

    # 获取优化显示的页码列表
    if page_all <= 2 + mid_pages:
        # 页码数少于6页就无需分析哪些地方需要隐藏
        page_range = list(page_xrange)
    else:
        # 添加应该显示的页码
        page_range += [1, page_all]
        page_range += [current_page - 1, current_page, current_page + 1, current_page + 2]
        if current_page - 2 >0:
            page_range.insert(0, current_page - 2)

        # 若当前页是头尾，范围拓展多1页
        if current_page == 1 or current_page == page_all:
            page_range += [current_page + 2, current_page - 2]

        # 去掉超出范围的页码
        page_range = filter(lambda x: x >= 1 and x <= page_all, page_range)

        # 排序去重
        page_range = sorted(list(set(page_range)))

        # 查漏补缺
        # 从第2个开始遍历，查看页码间隔，若间隔为0则是连续的
        # 若间隔为1则补上页码；间隔超过1，则补上省略号
        t = 1
        for i in range(len(page_range) - 1):
            step = page_range[t] - page_range[t - 1]
            if step >= 2:
                if step == 2:
                    page_range.insert(t, page_range[t] - 1)
                else:
                    page_range.insert(t, 0)
                t += 1
            t += 1
    return page_range

def get_left(current_page, left, num_pages):
    """
    辅助函数，获取当前页码的值得左边两个页码值，要注意一些细节，比如不够两个那么最左取到2
    ，为了方便处理，包含当前页码值，比如当前页码值为5，那么pages = [3,4,5]
    """
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i - 1 for i in range(current_page, current_page - left, -1) if i - 1 > 1]
        l.sort()
        return l
    l = [i for i in range(current_page, current_page - left, -1) if i > 1]
    l.sort()
    return l


def get_right(current_page, right, num_pages):
    """
    辅助函数，获取当前页码的值得右边两个页码值，要注意一些细节，
    比如不够两个那么最右取到最大页码值。不包含当前页码值。比如当前页码值为5，那么pages = [6,7]
    """
    if current_page == num_pages:
        return []
    return [i + 1 for i in range(current_page, current_page + right - 1) if i < num_pages - 1]

