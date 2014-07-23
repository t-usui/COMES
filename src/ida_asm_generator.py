#!/usr/bin/env python
#-*- coding:utf-8 -*-

import commands

class IDAAsmGenerator(object):
    
    def __init__(self):
        self.ida_executable = '/Applications/idaq.app/Contents/MacOS/idaq'
    
    def __del__(self):
        pass
    
    def generate(self, file_name):
        generate_command = self.ida_executable + ' -B ' + file_name
        
if __name__ == '__main__':
    generator = IDAAsmGenerator()
    
    generator.generate('/Users/isc/Documents/Programs/Research/compiler_estimater/signature_matcher/assiral.exe')
        