#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re


class IDAFileParser(object):
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
        
    def update_disassemble_flag(self, line, flag):
        # patterns to detect the start and end of subroutines
        pattern_subroutine_start = '^sub_[0-9A-Z]+?\t.+'
        pattern_subroutine_end = '^sub_[0-9A-Z]+?\tendp'
        pattern_winmain_start = '^WinMain.+'
        pattern_winmain_end = '^WinMain\t\tendp'
        pattern_start_proc_near = '^.+(\t|\s)proc(\t|\s)(near|far).+'
        pattern_endp = '^.+(\t|\s)endp'
        pattern_start = '^start:'
        pattern_ends = '[a-zA-Z0-9]+\t\tends'
        
        # compile all patterns
        p_sub_start = re.compile(pattern_subroutine_start)
        p_sub_end = re.compile(pattern_subroutine_end)
        p_main_start = re.compile(pattern_subroutine_start)
        p_main_end = re.compile(pattern_subroutine_end)
        p_start_proc_near = re.compile(pattern_start_proc_near)
        p_endp = re.compile(pattern_endp)
        p_start = re.compile(pattern_start)
        p_ends = re.compile(pattern_ends)
        
        # switch the flag of state machine
        # flag = 0: go out of a subroutine
        # flag = 1: get into a subroutine
        if p_sub_start.search(line) is not None and flag == 0:
            flag = 1
        elif p_sub_end.search(line) is not None and flag == 1:
            flag = 0
        elif p_main_start.search(line) is not None and flag == 0:
            flag = 1
        elif p_main_end.search(line) is not None and flag == 1:
            flag = 0
        elif p_start_proc_near.search(line) is not None and flag == 0:
            flag = 1
        elif p_endp.search(line) is not None and flag == 1:
            flag = 0
        elif p_start.search(line) is not None and flag == 0:
            flag = 1
        elif p_ends.search(line) is not None and flag == 1:
            flag = 0
        else:
            pass
        
        return flag
        
    def extract_instruction(self, file_name):
        instruction_list = []
        pattern_instruction = '^\t\t([a-zA-Z0-9]+)(\t([a-zA-Z0-9:@_+\[\] ]+)(,\s([a-zA-Z0-9:@_+\[\] ]+))?)?'
        p_inst = re.compile(pattern_instruction)
        
        # state machine:
        # disas_flag = 0 -> not a instruction line (because it is out of subroutines)
        # disas_flag = 1 -> regard line as a instruction (because it is in subroutines)
        disas_flag = 0
        with open(file_name, 'r') as f:
            for line in f:
                if disas_flag == 1:
                    m = p_inst.search(line)
                    if m is not None:
                        # if start from 'db', 'dw', 'dd', regard as data, not a instruction
                        if m.group(1) != 'db' and m.group(1) != 'dw' and m.group(1) != 'dd':
                            opcode, operand1, operand2 = m.group(1), m.group(3), m.group(5)
                            instruction_list.append([opcode, operand1, operand2])
                # update disas_flag of state machine
                disas_flag = self.update_disassemble_flag(line, disas_flag)
                
        return instruction_list
    
    def extract_code_block(self, file_name):
        code_block_list = []
        pattern_subroutine = '^(WinMain|start|sub_[0-9A-Z]+?|[0-9a-z_@]+(\s|\t)+proc(\s|\t)+(near|far))'
        pattern_location = '^(loc_[0-9A-Z]+):.+'
        pattern_instruction = '^\t\t([a-zA-Z0-9]+)(\t([a-zA-Z0-9:@_+\[\] ]+)(,\s([a-zA-Z0-9:@_+\[\] ]+))?)?'
        
        p_inst = re.compile(pattern_instruction)
        p_sub = re.compile(pattern_subroutine)
        p_loc = re.compile(pattern_location)
        
        subroutine_name, location_name = None, None
        disas_flag = 0
        with open(file_name, 'r') as f:
            for line in f:
                disas_flag = self.update_disassemble_flag(line, disas_flag)
                if disas_flag == 1:
                    m = p_sub.search(line)
                    if m is not None:
                        subroutine_name = m.group(1)        # entry point of subroutine
                        location_name = None                # no location at first in subroutine
                    
                    m = p_loc.search(line)
                    if m is not None:
                        location_name = m.group(1)          # start of loc_xxxxxxxx
                        
                    m = p_inst.search(line)
                    if m is not None:
                        if m.group(1) != 'db' and m.group(1) != 'dw' and m.group(1) != 'dd':
                            code_block_list.append((subroutine_name, location_name))
        return code_block_list
                
    def extract_opcode(self, file_name):
        opcode_list = []
        instruction_list = self.extract_instruction(file_name)
        
        # extract only opcode part (instruction[0]) from instruction_list
        for instruction in instruction_list:
            opcode_list.append(instruction[0])
            
        return opcode_list
    
    def extract_api(self, file_name):
        api_list = []
        
        pattern = 'label: "([A-Za-z0-9_]+)"'
        p = re.compile(pattern)
        
        with open(file_name, 'r') as f:
            text = f.read()
        for line in text.split('\n'):
            m = p.search(line)
            if m is not None:
                api = m.group(1)
                
                # Except mangled user-defined functions
                if api.startswith('__Z') is False:
                    api_list.append(api)
                    
        return api_list

if __name__ == '__main__':
    parser = IDAFileParser()

    asm_file_dir = '..\\asm'
    
    """
    asm_file_list = os.listdir(asm_file_dir)
    for file_name in asm_file_list:
        print asm_file_dir + os.sep + file_name
        print parser.extract_instruction(asm_file_dir + os.sep + file_name)
        if parser.extract_opcode(asm_file_dir + os.sep + file_name) == []:
            print asm_file_dir + os.sep + file_name
    """
    
    asm_file_name = 'k-means_demo.asm'
    
    code_block_list = parser.extract_code_block(asm_file_dir + os.sep + asm_file_name)
#    instruction_list = parser.extract_instruction(asm_file_dir + os.sep +asm_file_name)
    
#    count = 0
#    for i in range(len(code_block_list)):
#        print code_block_list[i][0], code_block_list[i][1], instruction_list[i][0]
#        if instruction_list[i][0] == 'mov':
#            count += 1
#    print count
    print code_block_list