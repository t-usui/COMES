#!/usr/bin/env python
#-*- coding:utf-8 -*-

from database import DatabaseHandler
import nltk
import numpy

class FeatureExtractor(object):
    
    def __init__(self):
        self.opcode_variety_ = None
        self.ngram_variety_ = None
        
    def __del__(self):
        pass
    
    def set_opcode_variety(self, opcode_variety_list):
        self.opcode_variety_ = opcode_variety_list
        
    def set_opcode_variety_from_database(self):
        # Order of bag-of-instructions feature vector
        db_handler = DatabaseHandler()
        opcode_variety_list = db_handler.extract_opcode_variety()
        self.set_opcode_variety(opcode_variety_list)
        
    def set_ngram_variety(self, ngram_variety_list):
        self.ngram_variety_ = ngram_variety_list
        
    def set_ngram_variety_from_database(self, N):
        db_handler = DatabaseHandler()
        ngram_variety_list = db_handler.extract_ngram_variety(N)
        self.set_ngram_variety(ngram_variety_list)
        
    def reduce_ngram_variety(self, unfiltered_opcode_list):
        """
        Not tested yet
        """
        for ngram in self.ngram_variety_:
            filter_flag = True
            
            for opcode in ngram:
                if opcode in unfiltered_opcode_list:
                    filtered_flag = False
            
            if filter_flag is True:
                self.ngram_variety_.remove(ngram)
        
    def extract_bag_of_opcodes(self, opcode_sequence):
        each_opcode_count = {}
        bag_of_opcodes = []
        
        # count each instruction's appearance
        for opcode in opcode_sequence:
            if opcode in each_opcode_count:
                each_opcode_count[opcode] += 1
            else:
                each_opcode_count[opcode] = 1
        
        # construct bag-of-instructions feature vector by order defined by instruction_variety_
        for variety in self.opcode_variety_:
            if variety in each_opcode_count:
                bag_of_opcodes.append(each_opcode_count[variety])
            else:
                bag_of_opcodes.append(0)
        
        return bag_of_opcodes
    
    def extract_ngram_sequence(self, opcode_sequence, N):
        ngram_sequence = []
        
        ngram = []
        for i in range(len(opcode_sequence) - N):
            del ngram[:]
            for j in range(N):
                ngram.append(opcode_sequence[i + j])
            ngram_sequence.append(tuple(ngram))         # Convert to immutable object, tuple
            
        return ngram_sequence
    
    def extract_ngram_list(self, opcode_sequence, N):
        """
        Eliminate duplication from ngram_sequence
        """
        ngram_sequence = self.extract_ngram_sequence(opcode_sequence, N)
        ngram_list = list(set(ngram_sequence))          # eliminate duplication
        
        return ngram_list
       
    # def extract_ngram(self, opcode_sequence, subroutine_sequence, num):
    def extract_ngram(self, opcode_sequence, N, reduce_dimension=False, unfiltered_opcode_list=None):
        each_ngram_count = {}
        ngram_feature_vector = []
        
        ngram_sequence = self.extract_ngram_sequence(opcode_sequence, N)
        for ngram in ngram_sequence:
            if each_ngram_count.has_key(ngram):
                each_ngram_count[ngram] += 1
            else:
                each_ngram_count[ngram] = 1
                
        self.set_ngram_variety_from_database(N)
        
        # TODO: test around dimension reduction
        if reduce_dimension is True:
            if unfiltered_opcode_list is None:
                print 'Unfiltered opcode list is not specified'
                
                db_handler = DatabaseHandler()
                unfiltered_opcode_list = db_handler.extract_unfiltered_opcode()
                print 'Extracted from database'
                
            self.reduce_ngram_variety(unfiltered_opcode_list)
                
        for variety in self.ngram_variety_:     # set ngram_variety_ before here
            if variety in each_ngram_count:
                ngram_feature_vector.append(each_ngram_count[variety])
            else:
                ngram_feature_vector.append(0)
                
        return ngram_feature_vector
    
    def extract_sequence_length(self, sequence):
        length_list = []
        
        current_element = None
        length = 0
        for element in sequence:
            if current_element is None:
                current_element = element
            if current_element == element:
                length += 1
            else:
                length_list.append(length)
                current_element = element
                length = 1
                
        return length_list
    
    def extract_subroutine_length(self, subroutine_sequence):
        return self.extract_sequence_length(subroutine_sequence)
    
    def extract_basicblock_length(self, location_sequence):
        return self.extract_sequence_length(location_sequence)
    
    def calculate_average_sequence_length(self, length_list):
        length_array = numpy.array(length_list)
        average_sequence_length = numpy.average(length_array)
        
        return average_sequence_length
    
    def extract_average_subroutine_length(self, subroutine_sequence):
        subroutine_length_list = self.extract_subroutine_length(subroutine_sequence)
        average_subroutine_length = self.calculate_average_sequence_length(subroutine_length_list)
        
        return average_subroutine_length
    
    def extract_average_basicblock_length(self, location_sequence):
        basicblock_length_list = self.extract_basicblock_length(location_sequence)
        average_basicblock_length = self.calculate_average_basicblock_length(location_length_list)
        
        return average_basicblock_length
                    
    def your_feature_extraction_method_here(self):
        pass
    
    def extract_feature_vector(self, file_id, extraction_method):
        db_handler = DatabaseHandler()
        
        if self.opcode_variety_ is None:
            self.set_opcode_variety_from_database()
        
        opcode_sequence = db_handler.extract_opcode_sequence(file_id)
        if extraction_method == 'bag-of-opcodes':
            feature_vector = self.extract_bag_of_opcodes(opcode_sequence)
        elif extraction_method == '2-gram':
            feature_vector = self.extract_ngram(opcode_sequence, 2)
        elif extraction_method == '3-gram':
            feature_vector = self.extract_ngram(opcode_sequence, 3)
        elif extraction_method == 'proposed':
            subroutine_sequence = db_handler.extract_subroutine_sequence(file_id)
            average_subroutine_length = self.extract_average_subroutine_length(subroutine_sequence)
            location_sequence = db_handler.extract_location_sequence(file_id)
            average_basicblock_length = self.extract_average_basicblock_length(location_sequence)
            # construct feature_vector here
        else:
            sys.stderr.write('Error: no extraction method "' + extraction_method + '" found.')
            sys.exit()
        
        return feature_vector

if __name__ == '__main__':
    db_handler = DatabaseHandler()
    opcode_sequence = db_handler.extract_opcode_sequence(500)
    # bigrams = nltk.bigrams(opcode_sequence)
    # fd = nltk.FreqDist(bigrams)
    # cfd = nltk.ConditionalFreqDist(bigrams)
    # cfd[u'cmp'].plot(50)
    trigrams = nltk.trigrams(opcode_sequence)
    print list(trigrams)
    # fd = nltk.FreqDist(trigrams)
    cfd = nltk.ConditionalFreqDist(trigrams)
    cfd[u'cmp'].plot(50)