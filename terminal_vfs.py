import os
import argparse
import csv
from datetime import datetime
from pathlib import Path

class VFS:
    def __init__(self, physical_path):
        self.physical_path = physical_path
        self.filesystem = {}  # Здесь будет храниться вся VFS в памяти
        self.load_vfs()
    
    def load_vfs(self):
        """Рекурсивно загружает всю структуру директории в память"""
        if not os.path.exists(self.physical_path):
            raise FileNotFoundError(f"VFS path not found: {self.physical_path}")
        
        if not os.path.isdir(self.physical_path):
            raise ValueError(f"VFS path is not a directory: {self.physical_path}")
        
        print(f"Loading VFS from: {self.physical_path}")
        self.filesystem = self._load_directory(self.physical_path)
        print("VFS loaded successfully into memory!")
    
    def _load_directory(self, current_path):
        """Рекурсивно загружает директорию и все её содержимое"""
        vfs_node = {
            'type': 'directory',
            'content': {},
            'path': current_path,
            'name': os.path.basename(current_path)
        }
        
        try:
            for item_name in os.listdir(current_path):
                item_path = os.path.join(current_path, item_name)
                
                if os.path.isdir(item_path):
                    # Рекурсивно загружаем поддиректорию
                    vfs_node['content'][item_name] = self._load_directory(item_path)
                else:
                    # Загружаем файл в память
                    vfs_node['content'][item_name] = self._load_file(item_path)
                    
        except PermissionError:
            print(f"Permission denied reading: {current_path}")
        except Exception as e:
            print(f"Error reading {current_path}: {e}")
        
        return vfs_node
    
    def _load_file(self, file_path):
        """Загружает содержимое файла в память"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'type': 'file',
                'content': content,
                'size': len(content),
                'path': file_path,
                'name': os.path.basename(file_path)
            }
            
        except PermissionError:
            print(f"Permission denied reading file: {file_path}")
            return {
                'type': 'file',
                'content': '[PERMISSION DENIED]',
                'size': 0,
                'path': file_path,
                'name': os.path.basename(file_path)
            }
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return {
                'type': 'file',
                'content': f'[ERROR: {str(e)}]',
                'size': 0,
                'path': file_path,
                'name': os.path.basename(file_path)
            }
    
    def get_node(self, path="/"):
        """Возвращает узел по пути"""
        if path == "/":
            return self.filesystem
        
        parts = path.strip('/').split('/')
        current = self.filesystem
        
        for part in parts:
            if part in current['content']:
                current = current['content'][part]
            else:
                return None
        return current

class Terminal:
    
    def __init__(self):
        self.user = os.getenv('USER') or 'user'
        self.vfs = None
        self.current_vfs_path = "/"
        self.error_flag = False
        
        self.get_arguments()
        
    def get_prompt(self):
        """Формирует приглашение с учетом VFS"""
        if self.vfs:
            # Показываем текущий путь в VFS
            display_path = self.current_vfs_path if self.current_vfs_path != "/" else "/"
            return f"{self.user}@vfs-terminal:{display_path}$ "
        else:
            return f"{self.user}@terminal:~$ "
        
    def get_command(self, command):
        self.error_flag = False
        command = command.strip()
        
        if not command:
            return
            
        # Логируем команду
        try:
            self.logger(f"{datetime.now().replace(microsecond=0)} | {self.user} | {command}")
        except:
            pass

        # Обработка команды exit
        if command == "exit":
            exit()
        
        # Если VFS загружена, команды ls, cd, cat работают с VFS
        if self.vfs:
            if command == "ls":
                self.vfs_ls()
            elif command.startswith("ls "):
                path = command[3:].strip()
                self.vfs_ls(path)
            elif command == "cd":
                print("cd: missing operand")
                self.error_flag = True
            elif command.startswith("cd "):
                path = command[3:].strip()
                self.vfs_cd(path)
            elif command == "pwd":
                print(self.current_vfs_path)
            elif command.startswith("cat "):
                path = command[4:].strip()
                self.vfs_cat(path)
            elif command == "vfs-info":
                self.vfs_info()
            else:
                print(f"Command not found: {command}")
                self.error_flag = True
        else:
            # Базовые команды (без VFS)
            if command.startswith("$"):
                try:
                    var_name = command[1:].strip()
                    print(os.environ.get(var_name, f"Variable {var_name} not found"))
                except:
                    print("")
            elif command.startswith("echo"):
                if len(command) > 4:
                    text = command[5:]
                    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
                        text = text[1:-1]
                    print(text)
                else:
                    pass
        
            elif command.startswith("ls"):
                print("ls: -a -t -m")
            
            elif command.startswith("cd"):
                if len(command) == 2:
                    print("cd: missing operand")
                else:
                    print("cd: cd")

            elif command.startswith("ls "):
                path = command[3:].strip()
                self.vfs_ls(path)
            elif command == "cd":
                print("cd: missing operand")
                self.error_flag = True
            elif command.startswith("cd "):
                path = command[3:].strip()
                self.vfs_cd(path)
            elif command == "pwd":
                print(self.current_vfs_path)
            elif command.startswith("cat "):
                path = command[4:].strip()
                self.vfs_cat(path)
            elif command == "vfs-info":
                self.vfs_info()
            else:
                print(f"Command not found: {command}")
                self.error_flag = True

    def vfs_ls(self, path="."):
        """Показывает содержимое VFS директории (команда ls)"""
        try:
            # Определяем целевой путь
            if path == ".":
                target_path = self.current_vfs_path
            elif path.startswith("/"):
                target_path = path
            else:
                target_path = f"{self.current_vfs_path}/{path}".replace("//", "/")
            
            # Получаем узел
            node = self.vfs.get_node(target_path)
            
            if not node:
                print(f"ls: cannot access '{path}': No such file or directory")
                self.error_flag = True
                return
                
            if node['type'] != 'directory':
                print(f"ls: '{path}': Not a directory")
                self.error_flag = True
                return
                
            # Выводим содержимое
            for name in node['content'].keys():
                item = node['content'][name]
                if item['type'] == 'directory':
                    print(f"\033[94m{name}/\033[0m")  # Синий для папок
                else:
                    print(f"\033[92m{name}\033[0m")   # Зеленый для файлов
                
        except Exception as e:
            print(f"ls error: {e}")
            self.error_flag = True

    def vfs_cd(self, path):
        """Меняет текущую директорию в VFS (команда cd)"""
        try:
            if path == "..":
                # Поднимаемся на уровень выше
                if self.current_vfs_path == "/":
                    return
                parts = self.current_vfs_path.strip('/').split('/')
                new_path = "/" + "/".join(parts[:-1])
                if new_path == "":
                    new_path = "/"
            elif path == "~":
                new_path = "/"
            elif path.startswith("/"):
                new_path = path
            else:
                new_path = f"{self.current_vfs_path}/{path}".replace("//", "/")
            
            # Проверяем путь
            node = self.vfs.get_node(new_path)
            if not node:
                print(f"cd: no such directory: {path}")
                self.error_flag = True
                return
                
            if node['type'] != 'directory':
                print(f"cd: not a directory: {path}")
                self.error_flag = True
                return
                
            self.current_vfs_path = new_path
            
        except Exception as e:
            print(f"cd error: {e}")
            self.error_flag = True

    def vfs_cat(self, path):
        """Показывает содержимое файла (команда cat)"""
        try:
            if path.startswith("/"):
                file_path = path
            else:
                file_path = f"{self.current_vfs_path}/{path}".replace("//", "/")
            
            node = self.vfs.get_node(file_path)
            if not node:
                print(f"cat: {path}: No such file")
                self.error_flag = True
                return
                
            if node['type'] != 'file':
                print(f"cat: {path}: Is a directory")
                self.error_flag = True
                return
                
            print(node['content'])
            
        except Exception as e:
            print(f"cat error: {e}")
            self.error_flag = True

    def vfs_info(self):
        """Показывает информацию о VFS"""
        if not self.vfs:
            print("VFS not loaded")
            return
            
        print(f"VFS source: {self.vfs.physical_path}")
        print(f"Current VFS path: {self.current_vfs_path}")
        print("Use 'ls' to see contents, 'cd' to navigate, 'cat' to view files")

    def get_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--logfile', '-l', help="Path to log file")
        parser.add_argument('--script', '-s', help="Path to script")
        parser.add_argument('--vfs', help="Path to Virtual File System")
        
        args = parser.parse_args()
        
        # Обработка logfile
        if args.logfile:
            self.log_path = args.logfile
            # Создаем файл с заголовком
            with open(self.log_path, 'w', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "user", "command", "status"])
        
        # Обработка script
        if args.script:
            if os.path.exists(args.script):
                self.start_script = args.script
                print(f"Executing script: {self.start_script}")
                self.execute_script()
            else:
                print(f"Script not found: {args.script}")
        
        # Обработка VFS
        if args.vfs:
            try:
                self.vfs = VFS(args.vfs)
                print(f"VFS loaded successfully from: {args.vfs}")
                print("Commands ls, cd, cat, pwd now work with VFS")
            except Exception as e:
                print(f"Error loading VFS: {e}")
                print("Running without VFS support")

    def execute_script(self):
        """Выполняет команды из скрипта"""
        try:
            with open(self.start_script, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(f"{self.get_prompt()}{line}")
                        self.get_command(line)
                        if self.error_flag:
                            print("Script stopped due to error")
                            break
            print("Script execution completed")
        except Exception as e:
            print(f"Error executing script: {e}")

    def logger(self, to_write):
        """Логирует команду"""
        try:
            if hasattr(self, 'log_path'):
                status = "ERROR" if self.error_flag else "SUCCESS"
                log_data = [
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    self.user,
                    to_write.split('|')[-1].strip() if '|' in to_write else to_write,
                    status
                ]
                
                with open(self.log_path, 'a', encoding='UTF-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(log_data)
        except Exception as e:
            print(f"Logging error: {e}")

    def run(self):
        print("Terminal emulator started. Type 'exit' to quit.")
        if self.vfs:
            print("VFS enabled: ls, cd, pwd, cat commands work with virtual file system")
        
        while True:
            try:
                command_get = input(self.get_prompt())
                self.get_command(command_get)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    term = Terminal()
    term.run()