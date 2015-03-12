#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import sys
import types

class Database(object):
    
    def __init__(self):
        self.host_name_ = '127.0.0.1'
        # self.host_name_ = 'localhost'
        self.database_name_ = 'COMES'
        self.user_name_ = 'comes_operator'
        self.password_ = 'c0m35p@55w0rd'
        """
        self.database_name_ = 'Summer_intern2014'
        self.user_name_ = 'si2014_user'
        self.password_ = 's12014p@55w0rd'
        """
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

    def query_insert(self, sql_statement, overwrite=False):
        """
        TODO: overwrite the duplicated entry if overwrite=True 
        """
        if type(sql_statement) == types.ListType:
            for s in sql_statement:
                try:
                    self.cursor.execute(s)
                except MySQLdb.cursors.IntegrityError:
                    if overwrite == True:
                        pass
        else:
            try:
                self.cursor.execute(sql_statement)
            except MySQLdb.cursors.IntegrityError:
                if overwrite == True:
                    pass
        self.connector.commit()
        
    def query_create(self, sql_statement):
        self.cursor.execute(sql_statement)


class DatabaseConstructor(Database):
    
    def append_opcode_variety(self, opcode_list):
        sql_statement = 'INSERT IGNORE INTO opcode_variety (opcode_name) VALUES ("%s")'
        sql_statement_list = []
        
        for opcode in opcode_list:
            sql_statement_list.append(sql_statement % opcode)
        self.query_insert(sql_statement_list)
        
    def append_bigram_variety(self, bigram_list):
        sql_statement = 'INSERT IGNORE INTO bigram_variety (bigram1, bigram2) VALUES ("%s", "%s")'
        sql_statement_list = []
        
        for bigram in bigram_list:
            sql_statement_list.append(sql_statement % (bigram[0], bigram[1]))
        self.query_insert(sql_statement_list)
        
    def append_trigram_variety(self, trigram_list):
        sql_statement = 'INSERT IGNORE INTO trigram_variety (trigram1, trigram2, trigram3) VALUES ("%s", "%s", "%s")'
        sql_statement_list = []
        
        for trigram in trigram_list:
            sql_statement_list.append(sql_statement % (trigram[0], trigram[1], trigram[2]))
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
            
    def insert_code_block(self, file_name, code_block_list):
        sql_statement = 'INSERT INTO instruction_code_block (file_name, instruction_id, subroutine, location) VALUES ("%s", %d, "%s", "%s")'
        
        for id in xrange(len(code_block_list)):
            self.query_insert(sql_statement % (file_name,
                                               id,
                                               code_block_list[id][0],
                                               code_block_list[id][1]))
            
    def insert_compiler_information(self, file_name, compiler):
        sql_statement = 'INSERT INTO compiler_information (file_name, compiler) VALUES ("%s", "%s")'
        self.query_insert(sql_statement % (file_name, compiler))
        
    def insert_optimization_level_information(self, file_name, optimization_level):
        sql_statement = 'INSERT INTO optimization_level_information (file_name, optimization_level) VALUES ("%s", "%s")'
        self.query_insert(sql_statement % (file_name, optimization_level))

    def insert_string_signature(self, compiler, string_signature):
        sql_statement = 'INSERT INTO string_signature (compiler_name, string_signature) VALUES ("%s", "%s")'
        self.query_insert(sql_statement % (compiler, string_signature))
        
    def insert_string_signature_from_dict(self, string_signature_dict):
        for signature, compiler in string_signature_dict.items():
            self.insert_string_signature(compiler, signature)
        

class DatabaseHandler(Database):
        
    def extract_opcode_variety(self):
        opcode_variety = []
        sql_statement = 'SELECT opcode_name FROM opcode_variety ORDER BY id ASC'

        result = self.query_select(sql_statement)
        for row in result:
            opcode_variety.append(row[0])
        return opcode_variety
    
    def extract_ngram_variety(self, N):
        if N == 2:
            ngram_variety = self.extract_bigram_variety()
        elif N == 3:
            ngram_variety = self.extract_trigram_variety()
        else:
            print 'Error: no ngram_variety database for N=%d found' % N
            sys.exit()
        return ngram_variety
    
    def extract_bigram_variety(self):
        bigram_variety = []
        sql_statement = 'SELECT bigram1, bigram2 FROM bigram_variety ORDER BY id ASC'
        
        result = self.query_select(sql_statement)
        for row in result:
            bigram_variety.append((row[0], row[1]))
        return bigram_variety
    
    def extract_trigram_variety(self):
        trigram_variety = []
        sql_statement = 'SELECT trigram1, trigram2, trigram3 FROM trigram_variety ORDER BY id ASC'
        
        result = self.query_select(sql_statement)
        for row in result:
            trigram_variety.append((row[0], row[1], row[2]))
        return trigram_variety

    def extract_unfiltered_opcode(self):
        unfiltered_opcode_list = []
        sql_statement = 'SELECT opcode FROM unfiltered_opcode'
        
        result = self.query_select(sql_statement)
        for row in result:
            unfiltered_opcode_list.append(row[0])
        return unfiltered_opcode_list
        
    def extract_instruction_sequence(self, sql_statement):
        instruction_sequence = []

        result = self.query_select(sql_statement)
        for row in result:
            instruction_sequence.append(row[0])
        return instruction_sequence
    
    def extract_all_file_id(self):
        file_id_list = []
        sql_statement = 'SELECT id FROM file_name'
        
        result = self.query_select(sql_statement)
        for row in result:
            file_id_list.append(row[0])
        return file_id_list
    
    def lookup_id_from_file_name(self, file_name):
        sql_statement = 'SELECT id FROM file_name WHERE file_name = "%s"'
        
        id = self.query_select(sql_statement % file_name)
        return id[0][0]
    
    def extract_opcode_sequence(self, id = None, file_name = None):
        if id is None and file_name is None:
            sys.stderr.write('Error: id or file_name is required')
            sys.exit()
        elif file_name is not None:
            lookup_id = self.lookup_id_from_file_name(file_name)
            if id is not None and lookup_id != id:
                print 'Warning: id looked up from file name does not match specified id'
                print 'looked up id is adopted'
            id = lookup_id
            
        opcode_sequence = []
        sql_statement = 'SELECT opcode FROM instruction_sequence, file_name WHERE instruction_sequence.file_name = file_name.file_name AND id = %s'
        
        result = self.query_select(sql_statement % id)
        for row in result:
            opcode_sequence.append(row[0])
        return opcode_sequence
    
    def extract_subroutine_sequence(self, id = None, file_name = None):
        if id is None and file_name is None:
            sys.stderr.write('Error: id or file_name is required')
            sys.exit()
        elif file_name is not None:
            lookup_id = self.lookup_id_from_file_name(file_name)
            if id is not None and lookup_id != id:
                sys.stderr.write('Warning: id looked up from file name does not match specified id')
                sys.stderr.write('looked up id is adopted')
            id = lookup_id
            
        subroutine_sequence = []
        sql_statement = 'SELECT subroutine FROM instruction_code_block, file_name WHERE instruction_code_block.file_name = file_name.file_name AND file_name.id = %s'
        result = self.query_select(sql_statement % id)
        for row in result:
            subroutine_sequence.append(row[0])
        return subroutine_sequence
    
    def extract_location_sequence(self, id = None, file_name = None):
        if id is None and file_name is None:
            sys.stderr.write('Error: id or file_name is required')
            sys.exit()
        elif file_name is not None:
            lookup_id = self.lookup_id_from_file_name(file_name)
            if id is not None and lookup_id != id:
                sys.stderr.write('Warning: id looked up from file name does not match specified id')
                sys.stderr.write('looked up id is adopted')
            id = lookup_id
            
        location_sequence = []
        sql_statement = 'SELECT location FROM instruction_code_block, file_name WHERE instruction_code_block.file_name = file_name.file_name AND file_name.id = %s'
        result = self.query_select(sql_statement % id)
        for row in result:
            location_sequence.append(row[0])
        return location_sequence
    
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

    def extract_optimization_level(self, id = None, file_name = None):
        if id is None and file_name is None:
            print 'Error: id or file_name is required'
            sys.exit()
        elif file_name is not None:
            lookup_id = self.lookup_id_from_file_name(file_name)
            if lookup_id != id:
                print 'Warning: id looked up from file name does not match specified id'
                print 'looked up id is adopted'
            id = lookup_id
            
        sql_statement = 'SELECT optimization_level FROM optimization_level_information, file_name WHERE optimization_level_information.file_name = file_name.file_name AND id = %s'
        
        optimization_level = self.query_select(sql_statement % id)[0][0]
        return optimization_level
    
    def extract_string_signature(self):
        string_signature_dict = {}
        sql_statement = 'SELECT compiler_name, string_signature FROM string_signature'
        
        result = self.query_select(sql_statement)
        for row in result:
            compiler = row[0]
            signature = row[1]
            string_signature_dict[signature] = compiler
        return string_signature_dict
 