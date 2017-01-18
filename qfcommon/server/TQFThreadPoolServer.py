#coding : utf-8

import logging
import threading
import traceback
import Queue
from Queue import Empty

from thrift.server.TServer import TServer
from thrift.transport import TTransport

log = logging.getLogger()

class TQFThreadPoolServer(TServer):
    def __init__(self, *args, **kwargs):
        TServer.__init__(self, *args)
        self.threads = 10
        self._stop_flag = False
        self.clients = Queue.Queue()
        self._thread_pool = []

    def setThreadsNum(self, num):
        '''set threads num'''
        self.threads = num

    def workThread(self):
        while True:
            try:
                client = self.clients.get(timeout=1)
                self.serveClient(client)
            except Empty, e:
                if self._stop_flag:
                    break
            except Exception, x:
                log.warn(x)

    def stop(self):
        '''stop the server'''
        self._stop_flag = True
        self.serverTransport.close()
        log.debug("server going to stop")

    def serveClient(self, client):
        itrans = self.inputTransportFactory.getTransport(client)
        otrans = self.outputTransportFactory.getTransport(client)
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        oprot = self.outputProtocolFactory.getProtocol(otrans)
        try:
            while True:
                self.processor.process(iprot, oprot)
        except TTransport.TTransportException, tx:
            log.warn(tx)
        except Exception, x:
            logging.warn(x)

        itrans.close()
        otrans.close()


    def serve(self):
        for i in range(self.threads):
            try:
                t = threading.Thread(target=self.workThread)
                t.setDaemon(False)
                self._thread_pool.append(t)
                t.start()
            except:
                log.warn(traceback.format_exc())

        self.serverTransport.listen()
        '''until stop flag is seted'''
        while not self._stop_flag:
            try:
                client = self.serverTransport.accept()
                self.clients.put(client)
            except KeyboardInterrupt, e:
                log.debug('KeyboardInterrupt')
                raise e
            except:
                log.debug(traceback.format_exc())

        for t in self._thread_pool:
            t.join()

        log.debug("all thread exit")
