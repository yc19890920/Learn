import sys
import etcd

client = etcd.Client(
    host='192.168.1.24',
    port=2379,
    allow_reconnect=True)
# client.delete('/nodes/', recursive=True, dir=True)
client.write('/nodes/n1', 1)
print 'node n1 value is %s' % client.read('/nodes/n1').value
try:
    client.write('/nodes/n1', 3, prevExist=False)
except Exception as e:
    print e.message
print 'node n1 value is %s after prevExist=False' % client.read('/nodes/n1').value
try:
    client.write('/nodes/n1', 3, prevValue=2)
except Exception as e:
    print e.message
print 'node n1 value is %s after prevValue=2' % client.read('/nodes/n1').value
client.write('/nodes/n1', 3, prevValue=1)
print 'node n1 value is %s after prevValue=1' % client.read('/nodes/n1').value
client.write('/nodes/n2', 2)
r3 = client.read('/nodes/n2')
print 'node n2 value is %s' % r3.value
r3.value += "5"
client.update(r3)
r4 = client.read('/nodes/n2')
print 'node n2 value is %s after update' % r4.value
watcher = client.eternal_watch('/nodes/n1')
for rsp in watcher:
    print '/nodes/n1 value change to %s' % watcher.value
    sys.stdout.flush()