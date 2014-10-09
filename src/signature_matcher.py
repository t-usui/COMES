#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import platform
import re
import subprocess
import sys

BEELZEBUB_PATH = '..\\beelzebub.exe'
STRINGS_PATH = '..\\jstrings.exe'

class SignatureMatcher:
    
    def __init__(self):
        pattern_major_ = 'MajorLinkerVersion: (.+)'
        pattern_minor_ = 'MinorLinkerVersion: (.+)'
        self.p_major_ = re.compile(pattern_major_)
        self.p_minor_ = re.compile(pattern_minor_)
        
    def __del__(self):
        pass

    def match_linker_version(self, file_name):
        major = None
        minor = None
        
        result = subprocess.check_output(BEELZEBUB_PATH + ' ' + file_name)
        match = self.p_major_.search(result)
        if match is not None:
            major = match.group(1)
        match = self.p_minor_.search(result)
        if match is not None:
            minor = match.group(1)
        return self.distinguish_linker_version(major, minor)

    def distinguish_linker_version(self, major, minor):
        if major is not None and minor is not None:
            major = major.rstrip(os.linesep)
            minor = minor.rstrip(os.linesep)
            
            if major == '2' and minor == '19':
                compiler_name = 'Delphi'
            elif major == '2' and minor == '17':
                compiler_name = 'MinGW'
            elif major == '5' and minor == '0':
                compiler_name = 'Borland C/C++'
            elif major == '5' and minor == 'c':
                compiler_name = 'MASM/TASM/FASM'
            elif major == '6' and minor == '0':
                compiler_name = 'Microsoft Visual C/C++ 6.0 (Visual Studio 6.0)'
            elif major == '7' and minor == '0':
                compiler_name = 'Microsoft Visual C/C++ 7.0 (Visual Studio.NET 2002)'
            elif major == '7' and minor == 'a':
                compiler_name = 'Microsoft Visual C/C++ 7.1 (Visual Studio.NET 2003)'
            elif major == '8' and minor == '0':
                compiler_name = 'Microsoft Visual C/C++ 8.0 (Visual Studio 2005)'
            elif major == '9' and minor == '0':
                compiler_name = 'Microsoft Visual C/C++ 9.0 (Visual Studio 2008)'
            else:
                print 'Unknown linker version detected'
                return
            return compiler_name
        else:
            if major is None:
                print 'Error: could not extract major linker version'
            if minor is None:
                print 'Error: could not extract minor linker version'

    def match_string(self, file_name):
        pattern_msvc = 'This program cannot be run in DOS mode'
        pattern_delphi = 'This program must be run under Win32'
        p_vc = re.compile(pattern_msvc)
        p_delphi = re.compile(pattern_delphi)
        
        if platform.system() == 'Windows':
            # IF running on Windows, use jstrings.exe
            string_command = STRINGS_PATH + ' --ascii < ' + file_name
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            # If running on Linux or MacOSX, use strings command
            string_command = 'strings ' + file_name
        else:
            print 'Unknown OS detected'
            sys.exit()
            
        string_result = subprocess.check_output(string_command, shell=True)
        if p_vc.search(string_result) is not None:
            compiler_name = 'Microsoft Visual C++ or MinGW'
        elif p_delphi.search(string_result) is not None:
            compiler_name = 'Borland C/C++ or Delphi'
        else:
            compiler_name = 'Unknown'
        return compiler_name

    def match_full_signature(self, file_name):
        linker_version_result = self.match_linker_version(file_name)
        string_result = self.match_string(file_name)
        
        return linker_version_result, string_result
        # In production
        
    def estimate(self, path):
        if os.path.isfile(path):
            return self.match_full_signature(path)
        elif os.path.isdir(path):
            result_list = []
            for file_name in os.listdir(path):
                result = self.match_full_signature(os.path.join(path, file_name))
                result_list.append(result)
            return result_list
        else:
            print 'Error: Unknown file name or file path'
            sys.exit()

    def print_help_and_exit(self):
        print 'Error: argc'
        print 'Usage: python signature_matcher.py <file_name/directory_path>'
        sys.exit()

if __name__ == '__main__':
    matcher = SignatureMatcher()

    path = 'C:\\Users\\tusui\\git\\COMES\\beelzebub.exe'
    result = matcher.estimate(path)
    print result[0]
    print result[1]