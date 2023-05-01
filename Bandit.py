"""
  Run this file at first, in order to see what is it printng. Instead of the print() use the respective log level
"""
############################### LOGGER
import os
from abc import ABC, abstractmethod
from zenq.logger import CustomFormatter, bcolors
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO) # this on you need for you tests.
 # create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())

logger.addHandler(file_handler)
 
logger.addHandler(ch)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
 
def calc(a,b):
  logger.warning(f"{calc.__name__}")
  return a+b
 
calc(5,6)