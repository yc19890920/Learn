
import json
import urllib3

http = urllib3.PoolManager(100, timeout=urllib3.Timeout(connect=10, read=300))

# fields = {'sender': '', 'receiver': '', 'message': tpl.organize_msg(replace=True)}
# url = None
# r = http.request('POST', url, fields=fields)
# if r.status == 200:
#     j = json.loads(r.data)