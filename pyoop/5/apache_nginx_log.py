import re

apache_pattern = r'''(?P<remote_addr>[\d\.]{4,}) - - (?:\[(?P<datetime>[^\[\]]+)\]) "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+)'''
nginx_pattern =  r'''(?P<remote_addr>[\d\.]{7,}) - - (?:\[(?P<datetime>[^\[\]]+)\]) "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "[^"]+" "(?P<user_agent>[^"]+)"'''
apache_regex = re.compile(apache_pattern)
nginx_regex = re.compile(nginx_pattern)

apache_s = [
    '127.0.0.1 - - [19/Mar/2018:03:52:07 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=c77975a8-c461-11e7-8472-005056967c31.jpg&aid=1 HTTP/1.0" 200 142920',
    '127.0.0.1 - - [19/Mar/2018:03:52:07 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=cbd8f006-c461-11e7-828b-005056967c31.jpg&aid=1 HTTP/1.0" 200 18621',
    '127.0.0.1 - - [19/Mar/2018:03:52:08 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=c018eb72-c461-11e7-828b-005056967c31.jpg&aid=1 HTTP/1.0" 200 12049',
    '127.0.0.1 - - [19/Mar/2018:03:52:08 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=d19859b4-c461-11e7-a2b6-005056967c31.jpg&aid=1 HTTP/1.0" 200 12881',
    '127.0.0.1 - - [19/Mar/2018:03:52:08 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=e03ce386-c461-11e7-828b-005056967c31.jpg&aid=1 HTTP/1.0" 200 8951',
    '127.0.0.1 - - [19/Mar/2018:03:52:08 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=d69b4462-c461-11e7-961d-005056967c31.jpg&aid=1 HTTP/1.0" 200 23605',
    '127.0.0.1 - - [19/Mar/2018:03:52:08 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=da4b36c6-c461-11e7-afd2-005056967c31.jpg&aid=1 HTTP/1.0" 200 22984',
    '127.0.0.1 - - [19/Mar/2018:03:52:09 +0800] "GET /template/ajax_get_network_attach/?id=186765&ufile_name=c6fc515e-5cb0-11e7-88af-005056967c31.png&aid=1 HTTP/1.0" 200 8716',
    '127.0.0.1 - - [19/Mar/2018:03:52:09 +0800] "GET /template/ajax_get_network_attach/?id=186765&ufile_name=35c593f2-5cb6-11e7-bb32-005056967c31.png&aid=1 HTTP/1.0" 200 193967'
]
nginx_s = [
    '103.250.230.38 - - [19/Mar/2018:03:49:11 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=da4b36c6-c461-11e7-afd2-005056967c31.jpg&aid=1 HTTP/1.1" 200 23020 "-" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Microsoft Outlook 14.0.7194; ms-office; MSOffice 14)" "-"',
    '103.250.230.38 - - [19/Mar/2018:03:49:11 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=d19859b4-c461-11e7-a2b6-005056967c31.jpg&aid=1 HTTP/1.1" 200 12909 "-" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Microsoft Outlook 14.0.7194; ms-office; MSOffice 14)" "-"',
    '103.250.230.38 - - [19/Mar/2018:03:49:11 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=e03ce386-c461-11e7-828b-005056967c31.jpg&aid=1 HTTP/1.1" 200 8971 "-" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Microsoft Outlook 14.0.7194; ms-office; MSOffice 14)" "-"',
    '103.250.230.38 - - [19/Mar/2018:03:49:12 +0800] "GET /template/ajax_get_network_attach/?id=215692&ufile_name=cbd8f006-c461-11e7-828b-005056967c31.jpg&aid=1 HTTP/1.1" 200 18649 "-" "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; Microsoft Outlook 14.0.7194; ms-office; MSOffice 14)" "-"',
    '204.79.180.16 - - [19/Mar/2018:03:49:18 +0800] "GET /new_track/t3/MjAxODAzMTQxMzU2NTQtMjk4MS00OHx8bGl1aHVhbmh1YW41QGh1YXdlaS5jb218fGh0dHA6Ly93d3cuY2l0ZXhwby5vcmcvc2hvd2luZm8xNDU2Ni5odG1sfHwxMDY5ODAw HTTP/1.1" 302 0 "-" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)" "-"',
]

for i in apache_s:
    print(i)
    m = apache_regex.search(i)
    if m:
        print(m.groups())
        print(m.groupdict())

print("-----------------------------------")
for i in nginx_s:
    print(i)
    m = nginx_regex.search(i)
    if m:
        print(m.groups())
        print(m.groupdict())
