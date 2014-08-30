#!/usr/bin/env python
#-*- coding:utf-8 -*-

import csv
from database import DatabaseConstructor, DatabaseHandler
from feature_extractor import FeatureExtractor
from ida_asm_parser import IDAAsmParser
import os
import sys
import time


class DataProcessor(object):
    
    def __init__(self):
        self.csv_save_dir_name = '..' + os.sep + 'csv'
    
    def __del__(self):
        pass
    
    def extract_file_name_from_file_path(self, file_path):
        return file_path.split(os.sep)[-1]
    
    def update_database(self, file_path, compiler=None, optimization_level=None):
        file_name = self.extract_file_name_from_file_path(file_path)
        
        file_name += '_' + compiler + '_' + optimization_level
        
        parser = IDAAsmParser()
        extractor = FeatureExtractor()
        db_constructor = DatabaseConstructor()
        
        # Update file_name table
        db_constructor.insert_file_name(file_name)
        
        # Update instruction_sequence table
        instruction_list = parser.extract_instruction(file_path)
        db_constructor.insert_instruction_sequence(file_name, instruction_list)
        
        # Update instruction_code_block table
        code_block_list = parser.extract_code_block(file_path)
        db_constructor.insert_code_block(file_name, code_block_list)
        
        # Update opcode_variety table
        opcode_list = parser.extract_opcode(file_path)
        db_constructor.append_opcode_variety(opcode_list)
        
        # Update bigram_variety table
        bigram_list = extractor.extract_ngram_list(opcode_list, 2)
        db_constructor.append_bigram_variety(bigram_list)
        
        # Update trigram_variety table
        trigram_list = extractor.extract_ngram_list(opcode_list, 3)
        db_constructor.append_trigram_variety(trigram_list)
        
        if compiler is not None:
            # Update compiler_information table
            db_constructor.insert_compiler_information(file_name, compiler)
        if optimization_level is not None:
            # Update optimization_level_information table
            db_constructor.insert_optimization_level_information(file_name, optimization_level)
            
    def update_database_from_dir(self):
        dir_name = '..' + os.sep + 'asm'
        
        for compiler in os.listdir(dir_name):
            for optimization_level in os.listdir(dir_name + os.sep + compiler):
                for file_name in os.listdir(dir_name + os.sep + compiler + os.sep + optimization_level):
                    self.update_database(dir_name + os.sep + compiler + os.sep + optimization_level + os.sep + file_name, compiler, optimization_level)
            
    def extract_data(self, id, extraction_method):
        extractor = FeatureExtractor()
        feature_vector = extractor.extract_feature_vector(id, extraction_method)
        
        # choose one of below
        label = self.extract_compiler_label(id)                 # for compiler estimation
        label = self.extract_optimization_level_label(id)       # for optimization level estimation
        
        return label, feature_vector
    
    def extract_all_data(self, extraction_method):
        label_list = []
        feature_vector_list = []
        
        db_handler = DatabaseHandler()
        file_id_list = db_handler.extract_all_file_id()
        
        for file_id in file_id_list:
            label, feature_vector = self.extract_data(file_id, extraction_method)
            feature_vector_list.append(feature_vector)
            label_list.append(label)
        
        return label_list, feature_vector_list
    
    def extract_compiler_label(self, file_id):
        db_handler = DatabaseHandler()
        
        compiler = db_handler.extract_compiler(file_id)
        if compiler == 'Borland C/C++':
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
        if optimization_level == 'O0':
            return 0
        elif optimization_level == 'O1':
            return 1
        elif optimization_level == 'O2':
            return 2
        elif optimization_level == 'O3':
            return 3
        else:
            print 'Error: unknown optimization level'
            sys.exit()
            
    @staticmethod
    def save_svmlight_format_file(file_name, label_list, feature_vector_list):
        f = open(file_name, 'w')
        
        if len(label_list) != len(feature_vector_list):
            print 'Error'
            sys.exit()
        
        with open(file_name, 'w') as f:
            for i in xrange(len(label_list)):
                line = ''
                # line = str(label_list[i])
                line = str(float(label_list[i]))
                
                dimension = 1
                for feature in feature_vector_list[i]:
                    if feature != 0:
                        line += ' '
                        # line += '%d:%d' % (dimension, feature)
                        line += '%d:%f' % (dimension, feature)
                    dimension += 1
                line += '\n'
                f.write(line)
        
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
        
if __name__ == '__main__':
    datproc = DataProcessor()
    
    # datproc.update_database('..\\asm\\MinGW\\O0\\astar_demo.asm', 'MinGW', 'O0')
    
    # dir_name = '..' + os.sep + 'asm' + os.sep + 'MinGW' + os.sep + 'O0'
    # for file_name in os.listdir(dir_name):
    #     save_file_name = file_name.split('.')[0] + '.csv'
    #     datproc.save_feature(file_name, save_file_name)
    label_list, feature_vector_list = datproc.extract_all_data('2-gram')
    for fv in feature_vector_list:
        print fv