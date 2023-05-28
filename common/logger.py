import logging
import sys

# for running
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(filename)s,%(lineno)d,%(funcName)s]"
                              "[tid:%(thread)d] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


if __name__ == '__main__':
    # test
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')