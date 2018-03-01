import logging
import inspect
import traceback

class bcolors:
    ERROR = '\033[91m' 
    DEBUG = '\033[0;33m'
    INFO = '\033[1;37m'
    TIME = '\033[0;32m'
    FILE = '\033[1;35m'
    PACK = '\033[1;33m'
    MESS = '\033[1;36m'
    ENDC = '\033[0m'

format = "[%(levelname)s] " + bcolors.TIME + "%(asctime)s " + bcolors.FILE + "%(file)s:%(line)s " + bcolors.ENDC + "in " + bcolors.PACK + "%(package)s\n " + bcolors.MESS + "-- %(message)s" + bcolors.ENDC


def summary(sfs):
    s = sfs.split(' ')
    d = {'file' : s[3][1:-2], 'line' : s[5][:-1], 'package' : s[7][:-1]}
    return d 

def stack_trace():
    frame = inspect.currentframe()
    return summary(traceback.format_stack(frame)[-3])

def stack_trace_from_exception(ex):
    lst = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    return summary(lst[1])

def debug(string):
    logging.basicConfig(format = bcolors.DEBUG + format, level = logging.DEBUG)    
    logging.debug(string, extra = stack_trace())

def info(string):
    logging.basicConfig(format = bcolors.INFO + format, level = logging.INFO)    
    logging.info(string, extra = stack_trace())

def exception(ex):
    string = "{0}: {1}".format(type(ex).__name__, ex.args[0])
    logging.basicConfig(format = bcolors.ERROR + format, level = logging.ERROR)
    logging.error(string, extra = stack_trace_from_exception(ex)) 
    
