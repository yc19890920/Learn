

### 浏览器接收通知（支持火狐、谷歌）

https://pushcrew.com

- [Introduction to REST API](http://api.pushcrew.com/docs/introduction-to-rest-api)
- [Segment Creator](https://support.pushcrew.com/support/solutions/articles/9000126137-segment-creator)
- [手把手教你如何增加网站的点击率？—Pushcrew的使用](https://baijia.baidu.com/s?old_id=807269)
- [手把手教你如何增加网站的点击率？—Pushcrew的使用](http://www.guxiaobei.com/how-to-use-pushcrew-to-increase-the-website-click-rate.html)
- [Top 15 Alternatives to PushEngage](http://www.pfind.com/alternatives/pushengage)


```
    <script type="text/javascript">
        (function(p,u,s,h){
            p._pcq=p._pcq||[];
            p._pcq.push(['_currentTime',Date.now()]);
            s=u.createElement('script');
            s.type='text/javascript';
            s.async=true;
            s.src='https://cdn.pushcrew.com/js/bc9c0262f45f3f1fccefdsfdsfsdfdsfds16565f1ac21bb.js';
            h=u.getElementsByTagName('script')[0];
            h.parentNode.insertBefore(s,h);
        })(window,document);
    </script>


import requests

headers = {}
headers.update({"Authorization": "a9b23bfdssdfds0c2b7d2dsdsadsf76c11fdf4f872d52e3462f"})
data = {
    "title": u"登录提醒",
    "message": u"这是一个测试",
    "url": u"https://www.bestedm.org",
}
# {"status":"success","segment_list":[{"id":"153228","name":"sale"},{"id":"153223","name":"service"}]}
def post():
    r = requests.post(
        # url="https://pushcrew.com/api/v1/send/all",
        # url="https://pushcrew.com/api/v1/send/segment/153223",
        url="https://pushcrew.com/api/v1/send/segment/153228",
        data=data,
        headers=headers,
    )
    print r.text
    print r.status_code

post()

# https://pushcrew.com/api/v1/segments/:segmentId/subscribers?page=1&per_page=2
# r = requests.get("https://pushcrew.com/api/v1/segments/153140/subscribers?page=1&per_page=6", headers=headers,)
# r = requests.get("https://pushcrew.com/api/v1/segments", headers=headers,)
# t = r.json()
# print r.json()
# print type(t)
```