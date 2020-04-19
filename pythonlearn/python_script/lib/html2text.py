#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

def beautifulsoup_html2text(html):
    # text = BeautifulSoup(html).get_text()
    text = BeautifulSoup(html, 'html5lib').get_text()
    return text

def re_html2tex(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.
    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"\n", " ", cleaned)
    return cleaned.strip()

if __name__ == '__main__':
    html = u"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <meta charset="utf-8" />
        <meta name="description" content="" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
    </head>
    <body>
        <div>
            <p style="color: red;">这是一个测试...</p>
        </div>
        <div>
            <div><img src="test/测试2016.png" border="0"></div>
        </div>
        </body>
    </html>
    """

    text = beautifulsoup_html2text(html).strip()
    # text = re_html2tex(html)
    print '----------------'
    print text
    print '----------------'
