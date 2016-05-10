import logging

logger = logging.getLogger('tsstats')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('debug.txt', 'w')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger.addHandler(fh)
logger.addHandler(ch)
