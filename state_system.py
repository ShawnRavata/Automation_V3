
class state_system():
    def __init__(self):
        self.output = {}
        self.state = 1

    def consume(self, output):
        self.output = output
        print(output)
        if(self.state == 1):
            print("I am here in mission 1")
        if(self.state == 2):
            print("Im here in mission 2")




