class Log():
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__file = open(self.__file_name, "a")
        self.__file.write("Log file created\n")
    
    def write(self, message):
        self.__file.write(message + "\n")
        