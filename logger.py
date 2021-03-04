from datetime import datetime

class log():

    def __init__(self):
        pass

    def startup(self):
        log = open("log.txt", "a") 
        log.write("\n--------------------iSeek Log--------------------\n")
        log.write("Application started at " + str(datetime.now()) + "\n")
        log.close()
    
    def endpointReached(self, name, ip):
        log = open("log.txt", "a")
        log.write(name + " endpoint reached at " + str(datetime.now()) + "\n")
        log.write("User IP: " + ip + "\n")
        log.close()

    def success(self):
        log = open("log.txt", "a")
        log.write("Successfully performed method\n")
        log.close()
    
    def fail(self, message):
        log = open("log.txt", "a")
        log.write("Failed to perform method\n")
        log.write("Error Code:\n")
        log.write(message)
        log.close()
    
    def write(self, message):
        log = open("log.txt", "a")
        log.write(message + "\n")
        log.close()