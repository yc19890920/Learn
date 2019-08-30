# -*- coding: utf-8 -*-
import os
import glob
# import errno
import random
from flask import Flask
from redis import Redis

app = Flask(__name__)

redis = Redis(host="flask-redis",port=6379)

@app.route('/')
def hi():
    r = (
        redis.pipeline()
            .incr("ping")
            .get("ping")
            .execute()
    )
    return 'hi , you have ping {0} times'.format(r[1])

@app.route('/file')
def gen_file():
    _dir = "/app/file"
    filelist = [os.path.join(_dir, fname) for fname
                in glob.glob1(_dir, '*%s' % ".txt")]
    num_entries = len(filelist)
    if num_entries >= 10:
        filelist = random.sample(filelist, int(num_entries / 3))
        for fname in filelist:
            try:
                os.remove(fname)
            except OSError as e:
                pass
                # if e.errno != errno.ENOENT:
                #     raise
    r = redis.incr("ping")
    with open("/app/file/{}.txt".format(r), 'wb') as f:
        f.write(str(r) + ".txt")
        return 'hi , you have ping file {0} times'.format(r)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

