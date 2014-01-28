#
from twisted.python import log

from multiprocessing import  Pool

from utils.misc import load_object

class ExecutionEngine(object):
    component_name = 'ExecuteEngine'

    def __init__(self, modules, extensions, poolsize=10):
        self.modules = modules
        self.extensions = extensions
        self.pool =  Pool(poolsize)

    @classmethod
    def from_settings(cls, settings):
        classes = settings.get('MODULES', {})
        modules = []
        for clspath, delay in classes.iteritems():
            clsobj = load_object(clspath)
            if hasattr(clsobj, 'from_settings'):
                obj = clsobj.from_settings(settings, delay)
            else:
                obj = clsobj(delay)
            modules.append(obj)

        enabled = [x.__class__.__name__ for x in modules]
        log.msg("Enabled modules: %s" %(", ".join(enabled), ))

        #load extensions
        classes = settings.get('EXTENSIONS', ()) 
        extensions = []
        for clspath in classes:
            clsobj = load_object(clspath)
            if hasattr(clsobj, 'from_settings'):
                obj = clsobj.from_settings(settings)
            else:
                obj = clsobj()
            extensions.append(obj)
        enabled_exts = [x.__class__.__name__ for x in extensions]  
        log.msg("Enable extensions: %s" % ", ".join(enabled_exts))

        poolsize = settings.get('MAX_PROCESS_NUM', 10) 

        return cls(modules, extensions, poolsize)

    def start(self):

        for module in self.modules:
            #reactor.callInThread(module.start)
            self.pool.map(module.start)

        log.msg("%s starts" % self.__class__.__name__)

    def stop(self):
        for module in self.modules:
            module.stop()
        log.msg("%s stop" % self.__class__.__name__)
