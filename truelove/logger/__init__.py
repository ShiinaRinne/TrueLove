import sys
from loguru import logger
from truelove.config import config

logger.remove()
logger.add(sys.stdout, level=config.log_level.upper())

logger.add("info.log", level='INFO', encoding='utf8')
logger.add("error.log", level='WARNING', encoding='utf8')

if config.log_level.upper() == "DEBUG":
    logger.add("debug.log", level='DEBUG', encoding='utf8')
    
    