#!/usr/bin/env python
#-*- coding:utf-8 -*-


import commands
import os

class SVMEstimator:
    
    def __init__(self):
        self.svm_tool_dir_path_ = '..' + os.sep + 'svm-tools' 
        self.learn_dir_path_ = '..' + os.sep + 'learn'
    
    def __del__(self):
        pass
    
    def train(self, training_set_file_name, model_file_name):
        training_set_file_name = self.learn_dir_path_ + os.sep + training_set_file_name
        model_file_name = self.learn_dir_path_ + os.sep + model_file_name
        train_command = self.svm_tool_dir_path_ + os.sep + 'svm-train ' + training_set_file_name + ' ' + model_file_name
        
        print commands.getoutput(train_command)
        
    def estimate(self, test_file_name, model_file_name, output_file_name):
        test_file_name = self.learn_dir_path_ + os.sep + test_file_name
        model_file_name = self.learn_dir_path_ + os.sep + model_file_name
        output_file_name = self.learn_dir_path_ + os.sep + output_file_name
        estimate_command = self.svm_tool_dir_path_ + os.sep + 'svm-predict '+ test_file_name + ' ' + model_file_name + ' ' + output_file_name
        
        print commands.getoutput(estimate_command)
        
    def scale(self, data_file_name, save_file_name):
        data_file_name = self.learn_dir_path_ + os.sep + data_file_name
        save_file_name = self.learn_dir_path_ + os.sep + save_file_name
        scale_command = self.svm_tool_dir_path_ + os.sep + 'svm-scale -s ' + save_file_name + ' ' + data_file_name
        
        print commands.getoutput(scale_command)
        
