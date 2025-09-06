import os
import subprocess


class Terminal:
    
    def __init__(self):
        self.user = os.popen('whoami').read().strip()
    
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
        
        elif command_get[0:5] == "echo ":
            command_get = command_get.replace('"', "")
            print(command_get[5:])

        elif command_get == "ls":
            print("ls: -1 -a -l -s -tn -sn ...")
        
        elif command_get == "cd":
            print("cd: -d, -e, -m ...")

    def run(self):
        while True:
            self.get_command()



if __name__ == "__main__":
    term = Terminal()
    term.run()
