#!/usr/bin/env python
#-*- coding:utf-8 -*-

from sklearn import cross_validation
from sklearn import datasets
from sklearn import ensemble
from sklearn import grid_search
from sklearn import metrics
from sklearn import svm
import numpy as np
import os
import subprocess


class Estimator(object):
    
    def __init__(self):
        self.base_model = None
        self.model = None
    
    def __del__(self):
        pass
    
    def set_base_model(self):
        """
        Should be overwritten by derived class
        """
        print 'Error: this method must be overwritten by derived class.'
        sys.exit()
    
    @staticmethod
    def calculate_accuracy(true_label, estimation_result_label):
        accuracy_score = metrics.accuracy_score(true_label, estimation_result_label)
        return accuracy_score
    
    def cross_validation(self):
        pass
    
    def conduct_grid_search(self, param_grid, training_data, training_label):
        if self.base_model is None:
            self.set_base_model()
        if self.base_model is None:
            print 'Error: set_base_model is not implemented properly.'
            sys.exit()
            
        clf = grid_search.GridSearchCV(self.base_model, param_grid, n_jobs=-1, cv=5, scoring='accuracy')
        clf.fit(training_data, training_label)
        
        print clf.grid_scores_
        print clf.best_estimator_
        print clf.best_score_
        print clf.best_params_
        print clf.scorer_
    
    def make_data_for_grid_search(self, data, test_size=0.2, random_state=0):
        development_set, evaluation_set = cross_validation.train_test_split(data, test_size, random_state)
        return development_set, evaluation_set
    
    
class SVMEstimator(Estimator):
    
    def set_base_model(self):
        self.base_model = svm.SVC()
    
    def train(self, training_data, training_label):
        model = svm.libsvm.fit(np.array(training_data),
                               np.float64(np.array(training_label)),
                               kernel='linear')
        self.model = model
        
    def estimate(self, test_data, model):
        result = svm.libsvm.predict(np.array(test_data),
                                    *self.model,
                                    kernel='linear')
        return result

    
class RandomForestEstimator(Estimator):
    
    def set_base_model(self):
        self.base_model = ensemble.RandomForestClassifier()
    
    def train(self, training_data, training_label):
        pass
    
    def estimate(self, test_data, model):
        pass
    
class BoostedDTEstimator(Estimator):
    
    def set_base_model(self):
        self.base_model = ensemble.AdaBoostClassifier()
    
    def train(self, training_data, training_label):
        pass
    
    def estimate(self, test_data, model):
        pass
    
class BoostedNBEstimator(Estimator):
    
    def train(self, training_data, training_label):
        pass
    
    def estimate(self, test_data, model):
        pass

class LIBSVMEstimator(object):
    
    def __init__(self):
        self.svm_tool_dir_path_ = '..' + os.sep + 'svm-tools' 
        self.learn_dir_path_ = '..' + os.sep + 'learn'
    
    def __del__(self):
        pass
    
    def set_parameter(self):
        pass
    
    def train(self, training_set_file_name, model_file_name):
        training_set_file_name = self.learn_dir_path_ + os.sep + training_set_file_name
        model_file_name = self.learn_dir_path_ + os.sep + model_file_name
        train_command = self.svm_tool_dir_path_ + os.sep + 'svm-train ' + training_set_file_name + ' ' + model_file_name
        
        print subprocess.check_output(train_command)
        
    def estimate(self, test_file_name, model_file_name, output_file_name):
        test_file_name = self.learn_dir_path_ + os.sep + test_file_name
        model_file_name = self.learn_dir_path_ + os.sep + model_file_name
        output_file_name = self.learn_dir_path_ + os.sep + output_file_name
        estimate_command = self.svm_tool_dir_path_ + os.sep + 'svm-predict '+ test_file_name + ' ' + model_file_name + ' ' + output_file_name
        
        print subprocess.check_output(estimate_command)
        
    def scale(self, data_file_name, save_file_name):
        data_file_name = self.learn_dir_path_ + os.sep + data_file_name
        save_file_name = self.learn_dir_path_ + os.sep + save_file_name
        scale_command = self.svm_tool_dir_path_ + os.sep + 'svm-scale -s ' + save_file_name + ' ' + data_file_name
        
        print subprocess.check_output(scale_command)

        
if __name__ == '__main__':    
    # estimator = SVMEstimator()
    estimator = RandomForestEstimator()
    
    """
    model = estimator.train(training_data, training_label)
    result = estimator.estimate(training_data, model)
    # print estimator.calculate_accuracy(training_label, result)
    """

    data_file = 'bag-of-opcodes.dat'    
    # data_file = '2-gram.dat'
    # data_file = '3-gram.dat'
    # data_file = '1-gram.txt'
    # data_file = '2-gram.txt'
    # data_file = '3-gram.txt'
    data_file_path = os.path.join('..', 'learn', data_file)

    feature_vector, label = datasets.load_svmlight_file(data_file_path)
    
    # estimator.set_base_model()
    # param_grid = {'kernel':('linear', 'rbf'), 'C':[1, 10, 100, 1000]}
    # param_grid = {'kernel':['rbf'], 'C':[0.01, 0.1, 1, 10, 100], 'gamma':[0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]}
    # param_grid = {'n_estimators':[5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'max_features':('auto', 'sqrt', 'log2', None)}
    param_grid = {'n_estimators':[5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'max_depth':[5, 7, 9, 11, 13, 15]}
    # param_grid = {'n_estimators':[10, 20, 30, 50, 70, 100]}
    # estimator.conduct_grid_search(param_grid, training_data, training_label)
    # development_data, evaluation_data, development_label, evaluation_label = cross_validation.train_test_split(training_data, training_label)
    # estimator.conduct_grid_search(param_grid, development_data, development_label)
    estimator.conduct_grid_search(param_grid, feature_vector.toarray(), label)