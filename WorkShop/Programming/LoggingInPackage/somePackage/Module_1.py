import time
from . import logger


class Timer(object):
    def __init__(self):
        self.t0 = time.time()

    def reset(self):
        self.t0 = time.time()
        logger.info('Timer reset at {}'.format(
            time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(self.t0))))

    def passed(self):
        passed = time.time() - self.t0
        logger.debug(f'Passed {passed} seconds.')
        return passed
