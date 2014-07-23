#!/usr/bin/env python
#-*- coding:utf-8 -*-

from database import Database
import copy

class FeatureExtractor(object):
    
    def __init__(self):
        self.opcode_variety_ = None
        
    def __del__(self):
        pass
    
    def set_opcode_variety(self, opcode_variety_list):
        self.opcode_variety_ = opcode_variety_list
        
    def set_opcode_variety_from_database(self):
        # Order of bag-of-instructions feature vector
        db = Database()
        self.opcode_variety_ = db.extract_opcode_variety()
        
    def extract_bag_of_opcodes(self, opcode_sequence):
        each_opcode_count = {}
        bag_of_opcodes = []
        
        # count each instruction's appearance
        for opcode in opcode_sequence:
            if opcode in each_opcode_count:
                each_opcode_count[opcode] += 1
            else:
                each_opcode_count[opcode] = 0 
        
        # construct bag-of-instructions feature vector by order defined by instruction_variety_
        for variety in self.opcode_variety_:
            if variety in each_opcode_count:
                bag_of_opcodes.append(each_opcode_count[variety])
            else:
                bag_of_opcodes.append(0)
        
        return bag_of_opcodes
        
    def extract_ngram(self, sequence, num):
        ngram = {}
        instructions = sequence.split('\n')
        instructions = self.append_curlybrace(instructions)

        for i in xrange(len(instructions)-num):
            line = ''
            for j in xrange(num):
                line += instructions[i + j]
            if ngram.has_key(line) is True:
                ngram[line] += 1
            else:
                ngram[line] = 1
        return ngram
    
    def append_curlybrace(self, lines):
        results = []
        for line in lines:
            results.append('{' + copy.deepcopy(line) + '}')
    
        return results
    
    def output_file(self, file_name, ngram):
        f = open(file_name, 'w')
        for k in ngram.keys():
            f.write(k)
        f.close()

if __name__ == '__main__':
#    extractor = FeatureExtractor()

#    file_name = 'file/test.dat'
#    f = open(file_name, 'r')
#    sequence = f.read()

#    ngram = extractor.extract_ngram(sequence, 2)
#    extractor.output_file('file/output.dat', ngram)

#    database_name = ''

#    f.close()
