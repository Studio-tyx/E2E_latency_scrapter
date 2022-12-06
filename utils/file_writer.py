import sys


class FileWriter:
    def __init__(self, path):
        self.path = path

    def write(self, string):
        stdout_backup = sys.stdout
        log_file = open(self.path, "a")
        sys.stdout = log_file
        print("writen log successfully: " + string)
        log_file.close()
        sys.stdout = stdout_backup
