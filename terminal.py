import os
import subprocess
import argparse
import csv
from datetime import datetime


class Terminal:
    
    def __init__(self):
        self.user = os.popen('whoami').read().strip()
        #self.log_path = os.path.join(os.getcwd(), "log.csv")
        self.start_script = ""
        self.get_arguments()
        self.vfs_path = ""
        
        
        
    def get_command(self):
        self.command_string = self.user + "@hostname:~$ "
        command_get = str(input(self.command_string))
        if command_get[0] == "$":
            try:
                print(os.environ[command_get[1:]])
            except:
                print("")
    
        elif command_get == "exit":
            exit()
        
        elif command_get[0:5] == "echo " and command_get[0] == '"' and command_get[-1] == '"':
            command_get = command_get.replace('"', "")
            print(command_get[5:])

        elif command_get == "ls":
            print("ls: -1 -a -l -s -tn -sn ...")
        
        elif command_get == "cd":
            print("cd: -d, -e, -m ...")

        self.logger(f"{self.user} | {datetime.now().replace(microsecond=0)} | {command_get}")


    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--verbose', '-v', help="полный вывод")
        parser.add_argument('--logfile', '-l', help="path to log file")
        args = parser.parse_args()
        if args.verbose:
            print("ok")
        if args.logfile:
            self.log_path = args.logfile
            with open(args.logfile, 'w', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)


    def logger(self, to_write):
        with open(self.log_path, 'a', encoding='UTF-8', newline='') as file:  # 'a' вместо 'w'
            writer = csv.writer(file)
            writer.writerow([to_write])

    def run(self):
        while True:
            self.get_command()


if __name__ == "__main__":
    term = Terminal()
    term.run()
