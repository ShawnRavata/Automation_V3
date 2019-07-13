from name_list import name_list

class logger_controller():
    def __init__(self):
        # get the name list
        self.name_list_class_obj = name_list()
        self.name_list = self.name_list_class_obj.get_name_string()
        self.name_list = ",".join(self.name_list) + '\n'
        # write to file
        self.file_stream = open('workfile.csv', 'w')
        self.file_stream.write(self.name_list)

    def consume(self, output):
        output = [str(val) for val in output.values()]
        log_message = ",".join(output) + '\n'
        self.file_stream.write(log_message)

    def __del__(self):
        self.file_stream.close()