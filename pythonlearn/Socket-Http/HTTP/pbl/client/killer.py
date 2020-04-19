# -*- coding: utf-8 -*-
#


from lib import core

if __name__ == "__main__":
    status, info = core.clean(clear_ip="61.144.162.26")
    print status
    print info