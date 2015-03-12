#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ida_asm_parser import IDAAsmParser
from database import DatabaseConstructor, DatabaseHandler
from data_processor import DataProcessor
from estimator import SVMClassifier, RandomForestClassifier
from estimator import BoostedNBClassifier, BoostedDTClassifier
from estimator import LogisticRegressionClassifier, LinearSVMClassifier
from estimator import NaiveBayesClassifier
from feature_extractor import FeatureExtractor
from sklearn import datasets
import argparse
import os
import sys


def updatedb(args):
    file_name = args.file_name
    dir_name = args.dir_name
    datproc = DataProcessor()
    
    if file_name is not None and dir_name is not None:
        sys.stderr.write('Error: please assign only one file name or directory name')
    elif file_name is not None:
        datproc.update_database_from_file(file_name)
    elif dir_name is not None:
        datproc.update_database_from_dir(dir_name)
    else:
        sys.stderr.write('Error: no file name or directory name specified')

def extract(args):
    output_file_name = args.output_file_name
    extraction_method = args.extraction_method
    label_type = args.label_type
    
    if output_file_name is None:
        sys.stderr.write('Error: no file name to output is specified')
        sys.exit()
    
    if extraction_method is None:
        extraction_method = '3-gram'        # default: 3-gram
        
    if label_type is None:
        label_type = 'compiler'             # default: compiler
    
    datproc = DataProcessor()
    datproc.save_all_data_in_svmlight_format(output_file_name,
                                             extraction_method, label_type)

def learn(args):
    algorithm = args.algorithm
    input_feature_file_name = args.input_feature_file_name
    param_grid_file_name = args.param_grid_file_name
    output_model_file_name = args.output_model_file_name
    
    if algorithm == 'SVM':
        estimator = SVMClassifier()
    elif algorithm == 'RF':
        estimator = RandomForestClassifier()
    elif algorithm == 'boost+NB':
        estimator = BoostedNBClassifier()
    elif algorithm == 'boost+DT':
        estimator = BoostedDTClassifier()
    elif algorithm == 'LR':
        estimator = LogisticRegressionClassifier()
    elif algorithm == 'LinearSVM':
        estimator = LinearSVMClassifier()
    elif algorithm == 'NB':
        estimator = NaiveBayesClassifier()
    else:
        sys.stderr.write('Error: no classifier %s found' % algorithm)
        sys.exit()
    
    try:
        feature_vector, label = datasets.load_svmlight_file(input_feature_file_name)
    except IOError:
        print 'Error: no file named %s found' % input_feature_file_name
        sys.exit()
        
    param_grid = estimator.load_param_grid(param_grid_file_name, algorithm)
    estimator.conduct_grid_search(param_grid, feature_vector.toarray(), label)
    estimator.dump_model(output_model_file_name)

def estimate(args):
    input_model_file_name = args.input_model_file_name
    input_exe_file_name = args.input_feature_file_name
    extraction_method = args.extraction_method
    label_type = args.label_type
    
    # generate an .asm file from the executable file
    generator = IDAAsmGenerator()
    generator.generate(input_exe_file_name)
    
    # append the information of the input file to the database
    datproc = DataProcessor()
    datproc.update_database_from_file()
    
    # extract feature vector
    ams_file_name = os.path.join(os.path.splittext(input_file_name)[0], '.asm')
    datproc.extract_data_from_file(asm_file_name, extraction_method,
                                   label_type)
    
    # load classification model
    estimator = CompilerEstimator()
    estimator.load_model(input_model_file_name)
    
    # estimate
    result = estimator.estimate(feature_vector)
    print result
    

if __name__ == '__main__':
    # the top-level parser
    argparser = argparse.ArgumentParser(prog='COMES',
                                        description='This is an fundamental compiler estimation program.')
    argparser.add_argument('-v',  # or '--version'
                           action='version',
                           version='Compiler Estimation Tool 1.0')
    
    subparsers = argparser.add_subparsers(help='sub-command help')
    
    # the parser for 'updatedb' command
    parser_updatedb = subparsers.add_parser('updatedb', help='a help')
    parser_updatedb.add_argument('-d',
                                 dest='dir_name',
                                 action='store',
                                 default=None,
                                 help='Assign the directory name to input'
                                 )
    parser_updatedb.add_argument('-f',
                                 dest='file_name',
                                 action='store',
                                 default=None,
                                 help='Assign the file name to input'
                                 )
    parser_updatedb.set_defaults(func=updatedb)
    
    # the parser for the 'extract' command
    parser_extract = subparsers.add_parser('extract', help='b help')
    parser_extract.add_argument('-o',
                                dest='output_file_name',
                                action='store',
                                default=None,
                                required=True,
                                help='Assign the file name to output extracted features'
                                )
    parser_extract.add_argument('-m',
                                dest='extraction_method',
                                action='store',
                                choices=['bag-of-opcodes', '2-gram', '3-gram'],
                                default=None,
                                help='extraction method (default 3-gram)'
                                )
    parser_extract.add_argument('-l',
                                dest='label_type',
                                action='store',
                                default=None,
                                help='label type (default compiler)'
                                )
    parser_extract.set_defaults(func=extract)
    
    # the parser for the 'learn' command
    parser_learn = subparsers.add_parser('learn', help='c help')
    parser_learn.add_argument('-a',
                              dest='algorithm',
                              action='store',
                              choices=['SVM', 'RF', 'boost+NB', 'boost+DT',
                                       'LR', 'LinearSVM', 'NB'],
                              default=None,
                              help='algorithm (default RF)'
                              )
    parser_learn.add_argument('-i',
                             dest='input_feature_file_name',
                             action='store',
                             default=None,
                             required=True,
                             help='input feature file name'
                             )
    parser_learn.add_argument('-o',
                              dest='output_model_file_name',
                              action='store',
                              default=None,
                              required=True,
                              help='output model file name'
                              )
    parser_learn.add_argument('-p',
                              dest='param_grid_file_name',
                              action='store',
                              default='../conf/grid_conf.json',
                              help='param grid file name'
                              )
    parser_learn.set_defaults(func=learn)
    
    # the parser for the 'estimate' command
    parser_estimate = subparsers.add_parser('estimate', help='d help')
    parser_estimate.add_argument('-m',
                              dest='input_model_file_name',
                              action='store',
                              default=None,
                              required=True,
                              help='input feature file name'
                              )
    parser_estimate.add_argument('-i',
                              dest='input_exe_file_name',
                              action='store',
                              default=None,
                              required=True,
                              help='input exe file name'
                              )
    parser_estimate.add_argument('-e',
                                dest='extraction_method',
                                action='store',
                                choices=['bag-of-opcodes', '2-gram', '3-gram'],
                                default=None,
                                help='extraction method (default 3-gram)'
                                )
    parser_estimate.add_argument('-l',
                                dest='label_type',
                                action='store',
                                default=None,
                                help='label type (default compiler)'
                                )
    parser_estimate.set_defaults(func=estimate)
    
    args = argparser.parse_args()
    args.func(args)
    
    """
    argparser.add_argument('-u',  # or '--update-db'
                           dest='update',
                           action='store_true',
                           default=False,
                           help='Insert new records of instruction sequence/compiler to the database.')
    argparser.add_argument('-e',  # or '--extract-feature'
                           dest='extract',
                           nargs=2,
                           action='append',
                           default=None,
                           help='Extract features from the database.')
    argparser.add_argument('-o',
                           dest='output',
                           action='store',
                           default=None,
                           help='Assign the file name to output.')
    argparser.add_argument('-l',  # or '--estimate'
                           dest='learn',
                           action='store_true',
                           default=False,
                           help='Estimate by machine learning techniques.')
    argparser.add_argument('-v',  # or '--version'
                           action='version',
                           version='Compiler Estimation Tool 1.0')
    
    parse_result = argparser.parse_args()
    
    datproc = DataProcessor()
    
    if parse_result.update is True:
        datproc.update_database_from_dir()
        
    if parse_result.extract is not None:
        extraction_method = parse_result.extract[0][0]
        label_type = parse_result.extract[0][1]
        if parse_result.output is not None:
            output_file_name = parse_result.output
            datproc.save_all_data_in_svmlight_format(output_file_name, extraction_method, label_type)
        else:
            print 'Error: no file name to output is specified'
            sys.exit()
            
    if parse_result.learn is True:
        estimator = RandomForestClassifier()
        
        data_file = '3-gram.dat'
        data_file_path = os.path.join('..', 'feature', data_file)
        model_file = 'test.model'
        model_file_path = os.path.join('..', 'model', model_file)
        feature_vector, label = datasets.load_svmlight_file(data_file_path)
        param_grid = {'n_estimators':[5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150], 'max_depth':[5, 7, 9, 11, 13, 15]}
        estimator.conduct_grid_search(param_grid, feature_vector.toarray(), label)
        estimator.dump_model(model_file_path)
        
    if parse_result.estimate is True:
        
            
    if parse_result.update is None and parse_result.extract is False:
        print 'No options are specified. Nothing to do.'
        sys.exit()
    """