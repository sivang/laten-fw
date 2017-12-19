
import inspect

def whoami():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller = calframe[1][3]
    del curframe
    del calframe
    return caller

def remote_debug():
    from laten.configregistry import Configuration
    c = Configuration()
    if not c.remote_debug:
        return
    from celery.contrib import rdb
    rdb.set_trace()
