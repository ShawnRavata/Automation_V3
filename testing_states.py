import threading
from queue import Queue
from pydispatch import dispatcher

class thread_1():
    def __init__(self):
        pass

    def update_state(self, state_list_q):
        print("I'm here")
        state_list = state_list_q.get()
        for i in range(len(state_list)):
            state_list[i] = not state_list[i]
        print("statelist in thread:", state_list)
        print("Task thread assigned to thread: {}".format(threading.current_thread().name))



class main_thread():
    def __init__(self):
        self.state_list = [True, False]
    def run_main(self):
        while True:
            if self.state_list[0] == True:
                print("we are in state 1")
            if self.state_list[1] == True:
                print("we are in state 2")
    def get_state_list(self):
        return self.state_list
    def update_statelist(self, variable):
        print("Task thread assigned to thread: {}".format(threading.current_thread().name))
        variable.get()
        if variable != None:
            self.state_list = variable

print("Task main thread assigned to thread: {}".format(threading.current_thread().name))
q = Queue()
main_object = main_thread()
q.put(main_object.state_list)
thread_1_object = thread_1()
t2 = threading.Thread(target=main_object.run_main)
t2.daemon=True
t2.start()
print("Im above threads")
print("main state_list:", main_object.state_list)
t1 = threading.Thread(target=thread_1_object.update_state, args =[q])
t1.daemon=True
t1.start()
print("main state_list:", main_object.state_list)

