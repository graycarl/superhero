import sys
import time
import logging


logger = logging.getLogger('supervisor')


class Supervisor:

    def run(self):
        logger.info('Start supervisor.')
        try:
            while True:
                time.sleep(.2)
        except KeyboardInterrupt:
            sys.stdout.write('\n')
            logger.info('Stop supervisor.')
            return
