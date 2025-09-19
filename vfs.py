import os
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
        
    
        
vfs = VFS('./vfs')
print(vfs.filesystem)
print("VFS loaded into memory!")
