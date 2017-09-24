import logging
import subprocess
import shlex


class Worker:
    logger = logging.getLogger('worker')

    def __init__(self, supervisor, name):
        self.name = name
        self.supervisor = supervisor
        self.running = False

    def start(self):
        pass

    def stop(self):
        pass


class SubprocessWorker(Worker):

    def __init__(self, supervisor, name, command):
        super(SubprocessWorker, self).__init__(supervisor, name)
        self.command = command
        self.process = None

    def __str__(self):
        cmd = self.command[:20]
        return '<{0.name} "{1}">'.format(self, cmd)

    def start(self):
        self.process = subprocess.Popen(
            shlex.split(self.command),
            # Start new session, so the supervisor's singal will not
            # passed to subprocess.
            start_new_session=True
        )
        self.running = True
        self.logger.info('%s is started. pid: %s', self, self.process.pid)

    def stop(self):
        self.logger.debug('%s: start to stop subprocess.', self)
        try:
            self.process.terminate()
            ret = self.process.wait(timeout=20)
            self.logger.debug(
                'Subprocess exit with code: %s', ret
            )
        except subprocess.TimeoutExpired:
            self.logger.info('%s: Terminate timeout, start to kill it.', self)
            self.process.kill()
            self.process.wait()
        self.running = False
        self.logger.info('%s is stoped.', self)
