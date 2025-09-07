import os
import subprocess
import argparse
import csv
from datetime import datetime


class Terminal:
    
    def __init__(self):
        self.user = os.popen('whoami').read().strip()
        self.command_string = self.user + "@hostname:~$ "

        #self.log_path = os.path.join(os.getcwd(), "log.csv")
        self.start_script = ""
        self.vfs_path = os.path.join(os.getcwd(), "vfs")

        self.get_arguments()
        
        
    def get_command(self, command):
        #command_get = str(input(self.command_string))
        if command[0] == "$":
            try:
                print(os.environ[command[1:]])
            except:
                print("")
    
        if command == "exit":
            exit()
        
        if command[0:5] == "echo ":
            command = command.replace('"', "")
            print(command[5:])

        if command == "ls":
            print("ls: -1 -a -l -s -tn -sn ...")
        
        if command == "cd":
            print("cd: -d, -e, -m ...")

        else:
            print(f"zsh: command not found: {command}")
            self.error_flag = True
        try:
            self.logger(f"{self.user} | {datetime.now().replace(microsecond=0)} | {command}")
        except:
            pass


    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--logfile', '-l', help="Path to log file")
        parser.add_argument('--script', '-s', help="Path to script")
        parser.add_argument('--vfs', '-vfs', help="Path to Virtual File System")
        args = parser.parse_args()


        if args.logfile:
            self.log_path = args.logfile
            with open(args.logfile, 'w', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)


        if args.script:
            self.start_script = args.script
            with open(self.start_script, 'r', encoding='UTF-8') as file:
                reader = csv.reader(file)
    
                for row in reader:
                    print(("".join(row)))
                    self.get_command("".join(row))

        if args.vfs:
            print(self.vfs_path)

    def logger(self, to_write):
        with open(self.log_path, 'a', encoding='UTF-8', newline='') as file:  # 'a' вместо 'w'
            writer = csv.writer(file)
            writer.writerow([to_write])


    def run(self):
        while True:
            command_get = str(input(self.command_string))
            self.get_command(command_get)



if __name__ == "__main__":
    term = Terminal()
    term.run()
