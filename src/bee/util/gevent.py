from gevent import monkey; monkey.patch_all()
import gevent

def patch_greenlet(f):
    def inner(*args, **kwargs):
         return gevent.spawn(f, *args, **kwargs)
    return inner