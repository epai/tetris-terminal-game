import logging

logger = logging.getLogger('tetris')
handler = logging.FileHandler('logs')
formatter = logging.Formatter('%(levelname)s - %(filename)s:%(lineno)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
