#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ida_asm_parser import IDAAsmParser
from database import Database
from feature_extractor import FeatureExtractor
from svm_estimator import SVMEstimator
import argparse
import os
import sys

def update_database(file_name, compiler=None):
    dir_path = '../asm'
    
    parser = IDAAsmParser()
    db = Database()
    
    db.insert_file_name(file_name)
    instruction_list = parser.extract_instruction(dir_path + os.sep + file_name)
    db.insert_instruction_sequence(file_name, instruction_list)
    opcode_list = parser.extract_opcode(dir_path + os.sep + file_name)
    db.append_opcode_variety(opcode_list)
    
    if compiler is not None:
        db.insert_compiler_information(file_name, compiler)
    
    del parser
    del db
    
def extract_data():
    feature_vector_list = []
    label_list = []
    
    feature_vector = extract_feature_vector()
    feature_vector_list.append(feature_vector)
    label = extract_label()
    label_list.append(label)
    
    return label_list, feature_vector_list
    
def extract_feature_vector():
    db = Database()
    extractor = FeatureExtractor()

    extractor.set_opcode_variety_from_database()    
    opcode_sequence = db.extract_opcode_sequence(1)
    bag_of_opcodes = extractor.extract_bag_of_opcodes(opcode_sequence)
    
    del db
    
    return bag_of_opcodes

def extract_label():
    db = Database()
    
    compiler = db.extract_compiler(1)

    del db
    if compiler == 'Borland C/C++':
        return 0
    elif compiler == 'Microsoft Visual C++':
        return 1
    elif compiler == 'MinGW':
        return 2
    else:
        print 'Error: unknown compiler'
        sys.exit()    

def output_file(file_name, label_list, feature_vector_list):
    f = open(file_name, 'w')
    
    if len(label_list) != len(feature_vector_list):
        print 'Error'
        sys.exit()

    for i in xrange(len(label_list)):
        line = ''
        line = str(label_list[i])
        
        dimension = 1
        for feature in feature_vector_list[i]:
            if feature != 0:
                line += ' '
                line += '%d:%d' % (dimension, feature)
            dimension += 1
        f.write(line)
    f.close()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Basic machine learning program.')
    argparser.add_argument('-u',  # or '--update-db'
                           dest='update',
                           nargs=2,
                           action='append',
                           default=None,
                           help='Insert new records of instruction sequence/compiler to the database.')
    argparser.add_argument('-e',  # or '--extract-feature'
                           dest='extract',
                           action='store_true',
                           default=False,
                           help='Extract features from the database.')
    argparser.add_argument('-o',
                           dest='output',
                           action='store',
                           default=None,
                           help='Assign the file name to output.')
    argparser.add_argument('-v',  # or '--version'
                           action='version',
                           version='SummerIntern Tool 1.0')
    
    parse_result = argparser.parse_args()
    
    if parse_result.update is not None:
        file_name = parse_result.update[0][0]
        compiler = parse_result.update[0][1]
        update_database(file_name, compiler)
        
    if parse_result.extract is True:
        label_list, feature_vector_list = extract_data()
        
        if parse_result.output is not None:
            output_file_name = parse_result.output
            output_file(output_file_name, label_list, feature_vector_list)
            
    estimator = SVMEstimator()
    estimator.scale('heart_scale', 'heart_scale.scale')
    estimator.train('heart_scale', 'heart_scale.model')
    estimator.estimate('heart_scale', 'heart_scale.model', 'heart_scale.output')
            
    if parse_result.update is None and parse_result.extract is False:
        print 'No options are specified. Nothing to do.'
        sys.exit()
