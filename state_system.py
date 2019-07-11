
class state_system():
    def __init__(self):
        self.output = {}
        self.state_1 = True
        self.state_2 = False

    def consume(self, output):
        self.output = output
        print(output)
        if(self.state_1):
            print("I am here", self.state_2)
            self.mission_1_object.mission_1_state(output)
        if(self.state_2):
            print("Im here in mission 2")




