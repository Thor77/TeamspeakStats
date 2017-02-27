# -*- coding: utf-8 -*-
import logging

# setup logger
logger = logging.getLogger('tsstats')
logger.setLevel(logging.INFO)

# define handlers
file_handler = logging.FileHandler('debug.txt', 'w', delay=True)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
