#!/usr/bin/env python
#-*- coding:utf-8 -*-

import csv
from database import DatabaseConstructor, DatabaseHandler
from feature_extractor import FeatureExtractor
from ida_asm_parser import IDAAsmParser
import os
import sys
from sklearn import datasets
import time


class DataProcessor(object):
    
    def __init__(self):
        self.csv_save_dir_name = os.path.join('..', 'csv')
    
    def __del__(self):
        pass
    
    def update_database_from_file(self,
                                  file_name,
                                  asm_file_path,
                                  gdl_file_path,
                                  compiler=None,
                                  optimization_level=None):
        file_name += '_' + compiler + '_' + optimization_level
        
        parser = IDAFileParser()
        extractor = FeatureExtractor()
        db_constructor = DatabaseConstructor()
        
        # Update file_name table
        db_constructor.insert_file_name(file_name)
        
        # Update instruction_sequence table
        instruction_list = parser.extract_instruction(asm_file_path)
        db_constructor.insert_instruction_sequence(file_name, instruction_list)
        
        # Update instruction_code_block table
        code_block_list = parser.extract_code_block(asm_file_path)
        db_constructor.insert_code_block(file_name, code_block_list)
        
        # Update opcode_variety table
        opcode_list = parser.extract_opcode(asm_file_path)
        db_constructor.append_opcode_variety(opcode_list)
        
        # Update bigram_variety table
        bigram_list = extractor.extract_ngram_list(opcode_list, 2)
        db_constructor.append_bigram_variety(bigram_list)
        
        # Update trigram_variety table
        trigram_list = extractor.extract_ngram_list(opcode_list, 3)
        db_constructor.append_trigram_variety(trigram_list)
        
        # Update api table
        api_list = parser.extract_api(gdl_file_path)
        db_constructor.insert_api(file_name, api_list)
        
        # Update api_variety table
        db_constructor.append_api_variety(api_list)
        
        if compiler is not None:
            # Update compiler_information table
            db_constructor.insert_compiler_information(file_name, compiler)
        if optimization_level is not None:
            # Update optimization_level_information table
            db_constructor.insert_optimization_level_information(file_name, optimization_level)
            
    def update_database_from_dir(self, dir_path):
        for compiler_name in os.listdir(dir_path):
            for optimization_level in os.listdir(os.path.join(dir_path, compiler_name)):
                for file_name in os.listdir(os.path.join(dir_path, compiler_name, optimization_level)):
                    asm_file_path = os.path.join(dir_path, compiler_name, optimization_level, file_name, file_name + '.asm')
                    gdl_file_path = os.path.join(dir_path, compiler_name, optimization_level, file_name, file_name + '.gdl')
                    self.update_database_from_file(file_name, asm_file_path, gdl_file_path, compiler_name, optimization_level)
            
    def extract_data(self, id, extraction_method, label_type):
        extractor = FeatureExtractor()
        feature_vector = extractor.extract_feature_vector(id, extraction_method)
        
        if label_type == 'compiler':
            label = self.extract_compiler_label(id)                 # for compiler estimation
        elif label_type == 'optimization_level':
            label = self.extract_optimization_level_label(id)       # for optimization level estimation
        elif label_type == 'test':
            return feature_vector                                   # for test data
        else:
            sys.stderr.write('Unknown label type specified')
            sys.exit()
        
        return label, feature_vector
    
    def extract_data_from_file(self, file_name, extraction_method, label_type):
        db_handler = DatabaseHandler()
        
        id = db_handler.lookup_id_from_file_name(file_name)
        label, feature_vector = self.extract_data(id, extraction_method,
                                                  label_type)
        
        return label, feature_vector
    
    def extract_all_data(self, extraction_method, label_type):
        label_list = []
        feature_vector_list = []
        
        # Extract all file ID from database
        db_handler = DatabaseHandler()
        file_id_list = db_handler.extract_all_file_id()
        
        for file_id in file_id_list:
            label, feature_vector = self.extract_data(file_id, extraction_method, label_type)
            feature_vector_list.append(feature_vector)
            label_list.append(label)
        
        return label_list, feature_vector_list
    
    def extract_compiler_label(self, file_id):
        db_handler = DatabaseHandler()
        
        compiler = db_handler.extract_compiler(file_id)
        if compiler == 'Borland C++ Compiler':
            return 0
        elif compiler == 'Microsoft Visual C++':
            return 1
        elif compiler == 'MinGW':
            return 2
        else:
            print 'Error: unknown compiler'
            sys.exit()
            
    def extract_optimization_level_label(self, file_id):
        db_handler = DatabaseHandler()
        
        optimization_level = db_handler.extract_optimization_level(file_id)
        if optimization_level == 'O0' or optimization_level == 'Od':
            return 0
        elif optimization_level == 'O1':
            return 1
        elif optimization_level == 'O2':
            return 2
        elif optimization_level == 'O3' or optimization_level == 'Ox':
            return 3
        else:
            print 'Error: unknown optimization level'
            sys.exit()
                
    def save_all_data_in_svmlight_format(self,
                                         file_path,
                                         extraction_method,
                                         label_type):
        label_list, feature_vector_list = self.extract_all_data(extraction_method, label_type)
        with open(file_path, 'wb') as f:
            datasets.dump_svmlight_file(feature_vector_list, label_list, f)
        
    def save_feature(self, file_name, save_file_name):
        db_handler = DatabaseHandler()
        
        opcode_variety = db_handler.extract_opcode_variety()

        opcode_sequence_O0 = db_handler.extract_opcode_sequence(file_name=file_name + '_MinGW_O0')
        opcode_sequence_O1 = db_handler.extract_opcode_sequence(file_name=file_name + '_MinGW_O1')
        opcode_sequence_O2 = db_handler.extract_opcode_sequence(file_name=file_name + '_MinGW_O2')
        opcode_sequence_O3 = db_handler.extract_opcode_sequence(file_name=file_name + '_MinGW_O3')
        
        with open(self.csv_save_dir_name + os.sep + save_file_name, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow([file_name, 'O0', 'O1', 'O2', 'O3'])
            for opcode in opcode_variety:
                row = []
                row.append(opcode)
                row.append(opcode_sequence_O0.count(opcode))
                row.append(opcode_sequence_O1.count(opcode))
                row.append(opcode_sequence_O2.count(opcode))
                row.append(opcode_sequence_O3.count(opcode))
                writer.writerow(row)
            row = []
            row.append('Sum')
            row.append(len(opcode_sequence_O0))
            row.append(len(opcode_sequence_O1))
            row.append(len(opcode_sequence_O2))
            row.append(len(opcode_sequence_O3))
            writer.writerow(row)
