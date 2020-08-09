from threading import Timer
from time import time


class UserTimer():
    def __init__(self, id, action):
        self.id = id
        self.currentTimeout = 180.0 * 60.0
        self.timestart = time()
        self.timeoutAction = action
        self.timer = Timer(self.currentTimeout, self.timeoutAction)
        self.timer.start()

    # time in seconds
    def penaltyTime(self, penalty):
        self.timer.cancel()
        self.currentTimeout -= (time() - self.timestart) + penalty
        self.timestart = time()
        if self.currentTimeout < 0:
            self.timeoutAction()
        else:
            self.timer = Timer(self.currentTimeout, self.timeoutAction, [self.id])

    # Returns time left in seconds
    def getTimeLeft(self):
        return self.currentTimeout - (time() - self.timestart)

    def stop(self):
        self.timer.cancel()