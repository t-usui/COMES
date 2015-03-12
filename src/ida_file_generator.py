#!/usr/bin/env python
#-*- coding:utf-8 -*-

import shutil
import subprocess
import os


class IDAFileGenerator(object):
    
    def __init__(self):
        self.ida_executable = '"D:\\exe_x86\\IDA 6.5\\idaq.exe"'
        self.exe_path = '..\\exe'
        self.asm_path = '..\\asm'
        self.gdl_path = '..\\gdl'
        
    def __del__(self):
        pass
    
    def generate(self, file_name):
        # generate .asm file
        self.generate_asm(file_name)
        self.move_asm(file_name)
        
        # generate .gdl file
        self.generate_gdl_gen_script_from_template(file_name)
        self.generate_gdl(file_name)
        self.move_gdl(file_name)
        
        # deletion and termination processing
        self.remove_gdl_gen_script()
        self.remove_idb(file_name)
    
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
        shutil.move(os.path.join(self.exe_path, asm_file_name),
                    os.path.join(self.asm_path, asm_file_name))
        
    def generate_gdl_gen_script_from_template(self, file_name, title=None):
        root, ext = os.path.splitext(file_name)
        gdl_file_name = root + '.gdl'
        
        if title is None:
            title = root
        
        with open('idapython_generate_gdl.tpl', 'r') as f:
            template = f.read()
        script = template.replace('file_name', '\'' + gdl_file_name + '\'')
        script = script.replace('title', '\'' + title + '\'')
        with open('idapython_generate_gdl.py', 'w') as f:
            f.write(script)
        
    def generate_gdl(self, file_name):
        root, ext = os.path.splitext(file_name)
        idb_file_name = root + '.idb'
        idb_file_full_path = os.path.abspath(os.path.join(self.exe_path, idb_file_name))
        
        gdl_gen_script = os.path.abspath('.\\idapython_generate_gdl.py')
        generate_command = self.ida_executable + ' -S"' + gdl_gen_script + '" ' + idb_file_full_path
        subprocess.check_output(generate_command, shell=True)
    
    def remove_gdl_gen_script(self):
        os.remove('idapython_generate_gdl.py')
        
    def move_gdl(self, file_name):
        root, ext = os.path.splitext(file_name)
        gdl_file_name = root + '.gdl'
        
        shutil.move(os.path.join(self.exe_path, gdl_file_name),
                    os.path.join(self.gdl_path, gdl_file_name))
        
if __name__ == '__main__':
    generator = IDAFileGenerator()
    
    for file_name in os.listdir('..\\exe'):
        print file_name
        generator.generate(file_name)