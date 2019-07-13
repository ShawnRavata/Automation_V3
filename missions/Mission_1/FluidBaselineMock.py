import threading
import time


class FluidBaselineMock:
    def __init__(self, state_obj):
        self.state_obj = state_obj

    def state_change(self, q):
        print("Task thread assigned to thread: {}".format(threading.current_thread().name))
        time.sleep(5)
        self.state_obj.q_set(2)
        time.sleep(3)
        self.state_obj.q_set(3)

    def threading_test(self):
        time.sleep(1)
        print("Task thread assigned to thread: {}".format(threading.current_thread().name))
