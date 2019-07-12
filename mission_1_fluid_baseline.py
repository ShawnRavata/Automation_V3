import time

class mission_1_test():
    def __init__(self):
        pass
    def state_change(self, q):
        time.sleep(5)
        state = q.get()
        state = 2