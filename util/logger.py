import logging
import sys
from colorama import Fore, Style
 
 
# 获取对象
def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
 
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)-9s %(asctime)s [%(module)s][%(funcName)s] line:%(lineno)d %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
 
log = get_logger()
 
def debug(msg):
    log.debug(Fore.WHITE + "[DEBUG]: " + str(msg) + Style.RESET_ALL)

def info(msg):
    log.info(Fore.GREEN + "[INFO]: " + str(msg) + Style.RESET_ALL)

def warning(msg):
    log.warning("\033[38;5;214m" + "[WARNING]: " + str(msg) + "\033[m")

def error(msg):
    log.error(Fore.RED + "[ERROR]: " + str(msg) + Style.RESET_ALL)

def critical(msg):
    log.critical(Fore.RED + "[CRITICAL]: " + str(msg) + Style.RESET_ALL)