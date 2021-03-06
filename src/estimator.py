#!/usr/bin/env python
#-*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import json
from sklearn import cross_validation
from sklearn import datasets
from sklearn import ensemble
from sklearn import grid_search
from sklearn import linear_model
from sklearn import metrics
from sklearn import naive_bayes
from sklearn import svm
from sklearn.externals import joblib
import numpy as np
import os
import subprocess
import sys


class Estimator(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    @abstractmethod
    def set_classifier(self, classifier):
        pass
    
    @abstractmethod
    def estimate(self, feature_value):
        pass
    

class CompilerEstimator(Estimator):
    
    def __init__(self, classifier=None):
        self.classifier = classifier
    
    def __del__(self):
        pass
    
    def set_classifier(self, classifier):
        self.classifier = classifier
        
    def estimate(self, feature_value):
        if self.classifier.model_ is None:
            sys.stderr.write('Error: please develop the model before estimation')
            sys.exit()
         
        result = self.classifier.classify(feature_value)
        return result


class OptimizationLevelEstimator(Estimator):
    
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def set_classifiers(self, classifier):
        self.first_layer_classifier = classifier[0]
    
    def first_layer_classification(self):
        pass
    
    def second_layer_classification(self):
        pass
    
    def estimate(self):
        pass


class Classifier(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.base_model_ = None
        self.model_ = None
    
    def __del__(self):
        pass
    
    @abstractmethod
    def set_base_model(self):
        """
        Should be overwritten by derived class
        """
        sys.stderr.write('Error: this method must be overwritten by derived class.')
        sys.exit()
    
    @staticmethod
    def calculate_accuracy(true_label, estimation_result_label):
        return metrics.accuracy_score(true_label, estimation_result_label)
    
    def cross_validation(self):
        pass
    
    def decode_list(self, data_list):
        decoded_list = []
        
        for item in data_list:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = _decode_list(item)
            elif isinstance(item, dict):
                item = _decode_dict(item)
            decoded_list.append(item)
            
        return decoded_list
    
    def decode_dict(self, data_dict):
        decoded_dict = {}
        
        for key, value in data_dict.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = self.value.encode('utf-8')
            elif isinstance(value, list):
                value = self.decode_list(value)
            elif isinstance(value, dict):
                value = self.decode_dict(value)
            decoded_dict[key] = value
        
        return decoded_dict
    
    def load_param_grid(self, file_name, algorithm):
        with open(file_name, 'r') as f:
            param_grid = json.load(f, object_hook=self.decode_dict)
        return param_grid[algorithm]
    
    def conduct_grid_search(self, param_grid, training_data, training_label):
        if self.base_model_ is None:
            self.set_base_model()
        if self.base_model_ is None:
            sys.stderr.write('Error: set_base_model is not implemented properly.')
            sys.exit()
            
        clf = grid_search.GridSearchCV(self.base_model_, param_grid, n_jobs=-1, cv=5, scoring='accuracy')
        clf.fit(training_data, training_label)
        self.model = clf.best_estimator_
        
        print clf.grid_scores_
        print clf.best_estimator_
        print clf.best_score_
        print clf.best_params_
        print clf.scorer_
    
    def make_data_for_grid_search(self, data, test_size=0.2, random_state=0):
        development_set, evaluation_set = cross_validation.train_test_split(data, test_size, random_state)
        return development_set, evaluation_set
    
    def dump_model(self, file_path):
        joblib.dump(self.model_, file_path)
        
    def load_model(self, file_path):
        self.model_ = joblib.load(file_path)

    
class SVMClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = svm.SVC()
    
    def train(self, training_data, training_label):
        model = svm.libsvm.fit(np.array(training_data),
                               np.float64(np.array(training_label)),
                               kernel='linear')
        self.model = model
        
    def classify(self, feature_vector):
        result = svm.libsvm.predict(np.array(test_data),
                                    *self.model_,
                                    kernel='linear')
        return result

    
class RandomForestClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = ensemble.RandomForestClassifier()
    
    def train(self, training_data, training_label):
        pass
    
    def estimate(self, test_data, model):
        pass
    
class BoostedDTClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = ensemble.AdaBoostClassifier()
    
    def train(self, training_data, training_label):
        pass
    
    def estimate(self, test_data, model):
        pass
    
class BoostedNBClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = ensemble.AdaBoostClassifier(base_estimator=naive_bayes.MultinomialNB())
    
    def train(self, training_data, training_label):
        pass
    
    def estimate(self, test_data, model):
        pass
    
    
class LogisticRegressionClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = linear_model.LogisticRegression()


class LinearSVMClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = svm.LinearSVC()
        

class NaiveBayesClassifier(Classifier):
    
    def set_base_model(self):
        self.base_model_ = naive_bayes.GaussianNB()

        
if __name__ == '__main__':    
    # estimator = SVMEstimator()
    estimator = RandomForestEstimator()
    
    """
    model = estimator.train(training_data, training_label)
    result = estimator.estimate(training_data, model)
    # print estimator.calculate_accuracy(training_label, result)
    """

    # data_file = 'bag-of-opcodes.dat'    
    # data_file = '2-gram.dat'
    data_file = '3-gram.dat'
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