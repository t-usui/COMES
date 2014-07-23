#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import sys
import types

class Database(object):
    
    def __init__(self):
        self.host_name_ = 'localhost'
        self.database_name_ = 'summer_intern2014'
        self.user_name_ = 'si2014_user'
        self.password_ = 's12O14p@55w0rd'
        self.connector = MySQLdb.connect(host = self.host_name_,
                                         db = self.database_name_,
                                         user = self.user_name_,
                                         passwd = self.password_,
                                         charset = 'utf8')
        self.cursor = self.connector.cursor()

    def __del__(self):
        self.cursor.close()
        self.connector.close()

    def query_select(self, sql_statement):
        self.cursor.execute(sql_statement)
        result = self.cursor.fetchall()
        return result

    def query_insert(self, sql_statement):
        if type(sql_statement) == types.ListType:
            for s in sql_statement:
                self.cursor.execute(s)
        else:
            print sql_statement
            self.cursor.execute(sql_statement)
        self.connector.commit()

    def extract_opcode_variety(self):
        opcode_variety = []
        sql_statement = 'SELECT opcode_name FROM opcode_variety ORDER BY id ASC'

        result = self.query_select(sql_statement)
        for row in result:
            opcode_variety.append(row[0])
        return opcode_variety

    def extract_instruction_sequence(self, sql_statement):
        instruction_sequence = []

        result = self.query_select(sql_statement)
        for row in result:
            instruction_sequence.append(row[0])
        return instruction_sequence
    
    def lookup_id_from_file_name(self, file_name):
        sql_statement = 'SELECT id FROM file_name WHERE file_name = "%s"'
        
        id = self.query_select(sql_statement % file_name)
        return id
    
    def extract_opcode_sequence(self, id = None, file_name = None):
        if id is None and file_name is None:
            print 'Error: id or file_name is required'
            sys.exit()
        elif file_name is not None:
            lookup_id = self.lookup_id_from_file_name(file_name)
            if lookup_id != id:
                print 'Warning: id looked up from file name does not match specified id'
                print 'looked up id is adopted'
            id = lookup_id
            
        opcode_sequence = []
        sql_statement = 'SELECT opcode FROM instruction_sequence, file_name WHERE instruction_sequence.file_name = file_name.file_name AND id = %s'
        
        result = self.query_select(sql_statement % id)
        for row in result:
            opcode_sequence.append(row[0])
        return opcode_sequence
    
    def extract_compiler(self, id = None, file_name = None):
        if id is None and file_name is None:
            print 'Error: id or file_name is required'
            sys.exit()
        elif file_name is not None:
            lookup_id = self.lookup_id_from_file_name(file_name)
            if lookup_id != id:
                print 'Warning: id looked up from file name does not match specified id'
                print 'looked up id is adopted'
            id = lookup_id
            
        sql_statement = 'SELECT compiler FROM compiler_information, file_name WHERE compiler_information.file_name = file_name.file_name AND id = %s'
        
        compiler = self.query_select(sql_statement % id)[0][0]
        return compiler
    
    def append_opcode_variety(self, opcode_list):
        sql_statement = 'INSERT IGNORE INTO opcode_variety (opcode_name) VALUES ("%s")'
        sql_statement_list = []
        
        for opcode in opcode_list:
            sql_statement_list.append(sql_statement % opcode)
        self.query_insert(sql_statement_list)
        
    def insert_file_name(self, file_name):
        sql_statement = 'INSERT INTO file_name (file_name) VALUES ("%s")'
        self.query_insert(sql_statement % file_name)
        
    def insert_instruction_sequence(self, file_name, instruction_list):
        sql_statement = 'INSERT INTO instruction_sequence (instruction_id, file_name, opcode, operand1, operand2) VALUES (%d, "%s", "%s", "%s", "%s")'
        
        for id in xrange(len(instruction_list)):
            self.query_insert(sql_statement % (id,
                                               file_name,
                                               instruction_list[id][0],
                                               instruction_list[id][1],
                                               instruction_list[id][2]))
            
    def insert_compiler_information(self, file_name, compiler):
        sql_statement = 'INSERT INTO compiler_information (file_name, compiler) VALUES ("%s", "%s")'
        self.query_insert(sql_statement % (file_name, compiler))

if __name__ == '__main__':
    sql_statement = 'hoge'
    db = Database()
    # db.query_insert(sql_statement)
