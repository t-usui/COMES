#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ida_asm_parser import IDAAsmParser
from database import DatabaseConstructor, DatabaseHandler
from data_processor import DataProcessor
from estimator import SVMClassifier, RandomForestClassifier
from estimator import BoostedNBClassifier, BoostedDTClassifier
from feature_extractor import FeatureExtractor
from sklearn import datasets
import argparse
import os
import sys


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Basic compiler estimation program.')
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
    argparser.add_argument('-l',  # or '--learn'
                           dest='learn',
                           action='store_true',
                           default=False,
                           help='Estimate by machine learning techniques.')
    argparser.add_argument('-v',  # or '--version'
                           action='version',
                           version='Compiler Estimation Tool 1.0')
    
    parse_result = argparser.parse_args()
    
    datproc = DataProcessor()
    
    if parse_result.update is not None:
        datproc.update_database_from_dir()
        
    if parse_result.extract is True:
        save_file_name = parse_result.output
        datproc.save_all_data_in_svmlight_format(output_file_name, label_list, feature_vector_list)
            
    if parse_result.learn is True:
        estimator = SVMEstimator()
        
        data_file = '2-gram.dat'
        data_file_path = os.path.join('..', 'learn', data_file)
        feature_vector, label = datasets.load_svmlight_file(data_file_path)
        param_grid = {'n_estimators':[5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'max_depth':[5, 7, 9, 11, 13, 15]}
        estimator.conduct_grid_search(param_grid, feature_vector.toarray(), label)        
            
    if parse_result.update is None and parse_result.extract is False:
        print 'No options are specified. Nothing to do.'
        sys.exit()