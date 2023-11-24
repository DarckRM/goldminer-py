import logging
import sys
from colorama import Fore, Style
 
 
# 获取对象
def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
 
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)-9s %(asctime)s [%(module)-10.10s][%(funcName)-16.16s] line:%(lineno)4d %(message)s")

        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger
 
log = get_logger()