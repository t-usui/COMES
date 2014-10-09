#!/usr/bin/env python
#-*- coding:utf-8 -*-

import shutil
import subprocess
import os


class IDAAsmGenerator(object):
    
    def __init__(self):
        self.ida_executable = 'C:\Program Files\IDA Free\idag.exe'
        self.exe_path = '..\exe'
        self.asm_path = '..\\asm'
        
    def __del__(self):
        pass
    
    def generate(self, file_name):
        self.generate_asm(file_name)
        self.remove_idb(file_name)
        self.move_asm(file_name)
    
    def generate_asm(self, file_name):
        generate_command = self.ida_executable + ' -B ' + os.path.join(self.exe_path, file_name)
        subprocess.check_output(generate_command)
        
    def remove_idb(self, file_name):
        # change the extension to '.idb'
        root, ext = os.path.splitext(file_name)
        idb_file_name = root + '.idb'
        
        # remove .idb file
        os.remove(os.path.join(self.exe_path, idb_file_name))
        
    def move_asm(self, file_name):
        # change the extension to '.asm'
        root, ext = os.path.splitext(file_name)
        asm_file_name = root + '.asm'
        
        # move .asm file from current directory to asm_path directory
        shutil.move(os.path.join(os.getcwd(), asm_file_name), os.path.join(self.asm_path, asm_file_name))
        
if __name__ == '__main__':
    generator = IDAAsmGenerator()
    
    generator.generate('Assiral_bcc.exe')