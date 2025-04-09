class Log():
    def __init__(self):
        self.__file_name = "data.txt"
        self.__file = open(self.__file_name, "a")
    
    def write(self, message):
        self.__file.write(message + "\n")