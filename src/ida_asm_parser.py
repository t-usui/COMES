#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

class IDAAsmParser(object):
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
        
    def update_disassemble_flag(self, line, flag):
        pattern_subroutine_start = '^sub_[0-9A-Z]+?\t.+'
        pattern_subroutine_end = '^sub_[0-9A-Z]+?\tendp'
        pattern_winmain_start = '^WinMain.+'
        pattern_winmain_end = '^WinMain\t\tendp'
        
        p_sub_start = re.compile(pattern_subroutine_start)
        p_sub_end = re.compile(pattern_subroutine_end)
        p_main_start = re.compile(pattern_subroutine_start)
        p_main_end = re.compile(pattern_subroutine_end)

        if p_sub_start.search(line) is not None and flag == 0:
            flag = 1
        elif p_sub_end.search(line) is not None and flag == 1:
            flag = 0
        elif p_main_start.search(line) is not None and flag == 0:
            flag = 1
        elif p_main_end.search(line) is not None and flag == 1:
            flag = 0
        else:
            pass
        
        return flag
        
    def extract_instruction(self, file_name):
        instruction_list = []
        pattern_instruction = '^\t\t([a-zA-Z0-9]+)(\t([a-zA-Z0-9]+)(, ([a-zA-Z0-9]+))?)?'
        p_inst = re.compile(pattern_instruction)
        
        f = open(file_name, 'r')
        
        disas_flag = 0
        for line in f:
            if disas_flag == 1:
                m = p_inst.search(line)
                if m is not None:
                    opcode, operand1, operand2 = m.group(1), m.group(3), m.group(5)
                    instruction_list.append([opcode, operand1, operand2])
            disas_flag = self.update_disassemble_flag(line, disas_flag)
        return instruction_list
    
    def extract_opcode(self, file_name):
        opcode_list = []
        
        instruction_list = self.extract_instruction(file_name)
        for instruction in instruction_list:
            opcode_list.append(instruction[0])
        return opcode_list

if __name__ == '__main__':
    parser = IDAAsmParser()
    print parser.extract_instruction('../file/Assiral_bcc.asm')
    print parser.extract_opcode('../file/Assiral_bcc.asm')
    