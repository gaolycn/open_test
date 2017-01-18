#coding : utf-8

import logging
import traceback
import os

from thrift.server.TServer import TServer
from thrift.transport import TTransport

log = logging.getLogger()

class TQFForkServer(TServer):
  def __init__(self, *args):
    TServer.__init__(self, *args)
    self.children = []

  def stop(self):
    '''stop the server'''
    self.serverTransport.close()
    log.debug("server going to stop")

  def serve(self):
    def try_close(file):
      try:
        file.close()
      except IOError:
        log.error(traceback.format_exc())

    self.serverTransport.listen()
    while True:
      client = self.serverTransport.accept()
      if not client:
        continue
      try:
        pid = os.fork()

        if pid:  # parent
          # add before collect, otherwise you race w/ waitpid
          self.children.append(pid)
          self.collect_children()

          # Parent must close socket or the connection may not get
          # closed promptly
          itrans = self.inputTransportFactory.getTransport(client)
          otrans = self.outputTransportFactory.getTransport(client)
          try_close(itrans)
          try_close(otrans)
        else:
          itrans = self.inputTransportFactory.getTransport(client)
          otrans = self.outputTransportFactory.getTransport(client)
          iprot = self.inputProtocolFactory.getProtocol(itrans)
          oprot = self.outputProtocolFactory.getProtocol(otrans)

          ecode = 0
          try:
            try:
              while True:
                self.processor.process(iprot, oprot)
            except TTransport.TTransportException:
              pass
            except Exception:
              log.error(traceback.format_exc())
              ecode = 1
          finally:
            try_close(itrans)
            try_close(otrans)

          os._exit(ecode)

      except TTransport.TTransportException:
        pass
      except Exception:
        log.error(traceback.format_exc())

  def collect_children(self):
    while self.children:
      try:
        pid, status = os.waitpid(0, os.WNOHANG)
      except os.error:
        pid = None

      if pid:
        self.children.remove(pid)
      else:
        break
