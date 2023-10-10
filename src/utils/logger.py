import logging
from enum import Enum

class LoggerLevel(Enum):
  DEBUG = 'debug'
  LOG = 'log'
  INFO = 'info'
  WARN = 'warn'
  ERROR = 'error'
  FATAL = 'fatal'


class Logger():
  def __init__(self,module):
    self.module = module
  
  def __msg__(self,msg,level = LoggerLevel.DEBUG):
    return f"[{self.module}] {level} : {msg}"

  def debug(self,msg):
    logging.debug(self.__msg__(msg,LoggerLevel.DEBUG))

  def log(self,msg):
    logging.log(self.__msg__(msg,LoggerLevel.LOG))

  def info(self,msg):
    logging.info(self.__msg__(msg,LoggerLevel.INFO))

  def warn(self,msg):
    logging.warn(self.__msg__(msg,LoggerLevel.WARN))

  def error(self,msg):
    logging.error(self.__msg__(msg,LoggerLevel.ERROR))

  def fatal(self,msg):
    logging.fatal(self.__msg__(msg,LoggerLevel.FATAL))
