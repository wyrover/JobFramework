#!/usr/bin/env python2.6
# encoding: utf-8
# Author: guodongdong <dd.guo@foxmail.com>
# Created Time: 2014年01月28日 星期二 10时45分39秒
from twisted.application import service
from twisted.python.logfile import DailyLogFile
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python import log

from core.engine import ExecutionEngine
from conf import settings

class Server(service.Service):

    def startService(self):
        service.Service.startService(self)
        engine = ExecutionEngine.from_settings(settings)
        engine.start()
        log.msg('start server')

    def stopService(self):
        log.msg('stop server')

def main():
    server = Server()
    application = service.Application(settings.get('PROJECT_NAME'))
    logfile = DailyLogFile(settings.get('LOG_FILE'), settings.get('LOG_DIR'))
    application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
    server.setServiceParent(application)
    from twisted.internet import reactor
    reactor.suggestThreadPoolSize(10)

if __name__ == "__main__":
    main()
