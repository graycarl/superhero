import sys
import time
import logging
from .worker import SubprocessWorker


class Supervisor:
    logger = logging.getLogger('supervisor')

    def __init__(self):
        self.workers = [
            SubprocessWorker(
                self, 'reverse-proxy',
                'gunicorn --workers 2 --bind localhost:8000 '
                'superhero.revproxy'),
            SubprocessWorker(
                self, 'sample-site',
                'gunicorn --workers 2 --bind localhost:8001 '
                'superhero.samplewsgi:app'),
            SubprocessWorker(
                self, 'console',
                'gunicorn --workers 2 --bind localhost:0 '
                'superhero.samplewsgi:app'),
        ]

    def start_workers(self):
        for worker in self.workers:
            if worker.running:
                continue
            worker.start()

    def stop_workers(self):
        for worker in self.workers:
            if not worker.running:
                continue
            worker.stop()

    def loop(self):
        self.logger.info('Start supervisor.')
        self.start_workers()
        try:
            while True:
                time.sleep(.2)
        except KeyboardInterrupt:
            sys.stdout.write('\n')
            self.logger.info('Stopping supervisor')
            self.stop_workers()
            self.logger.info('Exit.')
