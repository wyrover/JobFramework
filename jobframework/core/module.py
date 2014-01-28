# encoding: utf8


from twisted.internet import reactor
from twisted.python import log

class CallLaterOnce(object):
    """Schedule a function to be called in the next reactor loop, but only if
    it hasn't been already scheduled since the last time it run.
    """
    def __init__(self, func, *a, **kw):
        self._func = func
        self._a = a
        self._kw = kw
        self._call = None

    def schedule(self, delay=0):
        if self._call is None:
            self._call = reactor.callLater(delay, self)

    def cancel(self):
        if self._call:
            self._call.cancel()

    def __call__(self):
        self._call = None
        return self._func(*self._a, **self._kw)


class BaseModule(object):

    def __init__(self, delay):
        self.running = True
        self.delay = delay # seconds
        self.next_call = CallLaterOnce(self.__execute)
        log.msg("init %s, invoke every %s seconds" % \
            (self.__class__.__name__, delay))
        self.app_key= None
        self.app_secret = None
        self.call_back = None
        self.client = None

    def start(self):
        self.next_call.schedule()

    def stop(self):
        self.running = False

    def __execute(self):
        self.run()
        if self.running and self.delay > 0:
            self.next_call.schedule(self.delay)

    #interface
    def run(self):
        log.msg("%s run()" % self.__class__.__name__)

    def log(self, msg):
        log.msg("%s: %s" %(type(self), msg))

    def uni_to_utf8(self, unicode_attr):
        if isinstance(unicode_attr, unicode):
            result = unicode_attr.encode('UTF-8')
        elif isinstance(unicode_attr, list):
            result = []
            for key in unicode_attr:
                result.append(self.uni_to_utf8(key))
        elif isinstance(unicode_attr, dict):
            result = {}
            for key in unicode_attr:
                result[key.encode('UTF-8')] = self.uni_to_utf8(unicode_attr.get(key))
        elif isinstance(unicode_attr, str):
            result = unicode_attr
        else:
            result = str(unicode_attr)
        return result
