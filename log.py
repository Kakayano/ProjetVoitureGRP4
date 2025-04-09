from datetime import datetime

class Log():
    def __init__(self):
        self.__time = datetime.now()
        self.__time = self.__time.strftime("%Y-%m-%d")
        self.__file_name = "data.txt"
        self.__file = open(self.__file_name, "a")
    
    def write(self, message, type):
        self.__file.write( f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{type.upper()}] - {message}\n")

