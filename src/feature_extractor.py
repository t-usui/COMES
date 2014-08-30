#!/usr/bin/env python
#-*- coding:utf-8 -*-

from database import DatabaseHandler


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
        
    def set_ngram_variety_from_database(self, num):
        db_handler = DatabaseHandler()
        ngram_variety_list = db_handler.extract_ngram_variety(num)
        self.set_ngram_variety(ngram_variety_list)
        
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
    
    def extract_ngram_sequence(self, opcode_sequence, num):
        ngram_sequence = []
        
        ngram = []
        for i in range(len(opcode_sequence) - num):
            del ngram[:]
            for j in range(num):
                ngram.append(opcode_sequence[i + j])
            ngram_sequence.append(tuple(ngram))         # Convert to immutable object, tuple
            
        return ngram_sequence
    
    def extract_ngram_list(self, opcode_sequence, num):
        """
        Eliminate duplication from ngram_sequence
        """
        ngram_sequence = self.extract_ngram_sequence(opcode_sequence, num)
        ngram_list = list(set(ngram_sequence))          # eliminate duplication
        
        return ngram_list
       
    # def extract_ngram(self, opcode_sequence, subroutine_sequence, num):
    def extract_ngram(self, opcode_sequence, num):
        each_ngram_count = {}
        ngram_feature_vector = []
        
        ngram_sequence = self.extract_ngram_sequence(opcode_sequence, num)
        for ngram in ngram_sequence:
            if each_ngram_count.has_key(ngram):
                each_ngram_count[ngram] += 1
            else:
                each_ngram_count[ngram] = 1
                
        self.set_ngram_variety_from_database(num)
                
        for variety in self.ngram_variety_:     # set ngram_variety_ before here
            if variety in each_ngram_count:
                ngram_feature_vector.append(each_ngram_count[variety])
            else:
                ngram_feature_vector.append(0)
                
        return ngram_feature_vector
                    
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
        else:
            print 'Error: no extraction method "' + extraction_method + '" found.'
            sys.exit()
        
        return feature_vector


if __name__ == '__main__':
    extractor = FeatureExtractor()
    
    for i in range(1, 184):
        ngram = extractor.extract_feature_vector(i, 'bag-of-opcodes')
        print ngram