#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ida_asm_parser import IDAAsmParser
from database import Database

class OpcodeCollector:
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def register_from_ida_asm_file(self, file_name):
        parser = IDAAsmParser()
        db = Database()
        
        opcode_list = parser.extract_opcode(file_name)
        print opcode_list
        db.append_opcode_variety(opcode_list)
        
        del parser
        del db
        