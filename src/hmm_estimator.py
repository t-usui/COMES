#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ghmm import *
# from UnfairCasino import train_seq, test_seq
import sys
import database


class Estimator:
    def __init__(self):
        self.model_msvc = None
        self.model_bcc = None
        self.model_mingw = None
        self.lookup_table = None

    def define_emission_symbol(self, instruction_variety):
        # sigma = IntegerRange(1, 7)
        sigma = Alphabet(instruction_variety)
        return sigma

    def lookup_hidden_state_from_symbol(self, symbol):
        return self.lookup_table[symbol]

    def calculate_state_transition_matrix(self, observed_sequence_list):
        # A = [[0.9, 0.1], [0.3, 0.7]]
        # A = [[0.5, 0.5], [0.5, 0.5]]
        
        return A

    def calculate_symbol_emission_probability(self, observed_sequence_list, instruction_variety):
        each_instruction_count = {}
        emission_arithmetic_logic = []
        emission_data_transfer = []
        emission_brunch = []

        count = 0
        for instruction in observed_sequence:
            if instruction in each_instruction_count:
                each_instruction_count[instruction] += 1
            else:
                each_instruction_count[instruction] = 0
            count += 1

        for instruction in instruction_variety:
            if self.lookup_hidden_state_from_symbol(instruction) == 'state_arithmetic_logic':
                emission_arithmetic_logic.append(each_instruction_count[instruction]/count)
                emission_data_transfer.append(0)
                emission_brunch.append(0)
            elif self.lookup_hidden_state_from_symbol(instruction) == 'state_data_transfer':
                emission_arithmetic_logic.append(0)
                emission_data_transfer.append(each_instruction_count[instruction]/count)
                emission_brunch.append(0)
            elif self.lookup_hidden_state_from_symbol(instruction) == 'state_brunch':
                emission_arithmetic_logic.append(0)
                emission_data_transfer.append(0)
                emission_brunch.append(each_instruction_count[instruction]/count)

        B = [emission_arithmetic_logic, emission_data_transfer, emission_brunch]
        return B

    def calculate_initial_state_probability_vector(self, observed_sequence_list):
        each_state_count = {}
        pi = [] # Initial State Probability Vector

        count = 0
        for seq in observed_sequence_list:
            initial_instruction = seq[0]
            initial_state = self.lookup_hidden_state_from_symbol(initial_instruction)
            if initial_state in each_state_count:
                each_state_count[initial_state] += 1
            else:
                each_state_count[initial_state] = 0
            count += 1
        pi = [each_state_count['state_arithmetic_logic']/count, each_state_count['state_data_transfer']/count, each_state_count['state_brunch']/count]

        return pi

    def learn_model(self, instruction_sequence, train_seq):
        # Emission Symbol
        sigma = self.define_emission_symbol(instruction_sequence)

        # State Transition Matrix
        A = self.calculate_state_transition_matrix()
        # Symbol Emission Probability
        B = self.calculate_symbol_emission_probability()
        # Initial State Probability Vector
        pi = self.calculate_initial_state_probability_vector()

        model = HMMFromMatrices(sigma, DiscreteDistribution(sigma), A, B, pi)
        model.baumWelch(train_seq)
        print model

        return model

    def save_model(self, file_name):
        if self.model is not None:
            f = open(file_name, 'w')

        else:
            print 'Error: no model is found.'
            sys.exit()

    def load_model(self, file_name):
        f = open(file_name, 'w')

    def calculate_loglikelihood(self, test_seq, model):
        s5 = EmissionSequence(IntegerRange(1, 7),[1,2]*6)
        print str(s5)
        p = model.loglikelihood(s5)
        print p
        pass

    def estimate(self):
        pass

if __name__ == '__main__':
    observed_seq = ['mov', 'ret']

    est = Estimator()
    db = Database()

    model = e.learn_model(test_seq)
#    e.calculate_loglikelihood(test_seq, model)

# print m
# print test_seq

# v = m.viterbi(test_seq)
# print v


# my_seq = EmissionSequence(sigma, [1]*20+[6]*10+[1]*40)
# print my_seq
# print m.viterbi(my_seq)

# obs_seq = m.sampleSingle(20)
# obs = map(sigma.external, obs_seq)
# print obs

