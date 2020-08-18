# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 14:15:25 2020

@author: Patrick

This program attempts to figure out the optimal batch size for testing
The basics go like this: 
    Any given person being tested has a percent liklihood of testing positive
    We take the tests and batch process them. That means that we 
    process a whole bunch together.  If the results of the batch test
    come back negative, then they are all negative.
    If the results come back positive, then at least one member of the 
    group is positive.  We then process each sample from the group 
    idividually.  The total number of tests is the number of batches + the 
    number of individuals we had to retest.
    
    How does this save resources?  
    Let's do an example.  
    Let's assume there are 100 people who were tested, and 2% of them are 
    positive. 
    
    If we test them individually, that is 100 tests.
    
    Instead, let's group them into batches of 20.  That makes 5 batches. On 
    average, 3 of those batches will come back negative, and 2 will come back 
    positive.  We re-test those individuals in the positive group. 
    
    Total number of tests: 5 batch tests + 40 individual tests = 45
    
    
    If instead, we grouped them into batches of 10 people, then 8 of the 
    groups will come back negative, and 2 of the groups will come back 
    positive, requiring us to re-process the group members' tests.
    
    Total number of tests: 10 batch tests + 20 individual tests = 30 tests.
    
    Of course, the optimal batch size changes based on the percent positive.

"""

import matplotlib.pyplot as plt
from math import ceil
import numpy as np

Num_of_tests = 1e6  
batch_size = list(range(2,11))
percent_positive = list(range(1,11))  #This assumes we know what percent of tests come back positive.
leg = []

leg2=[]
data_array = np.zeros((len(batch_size), len(percent_positive)))
data_array_with_false = np.zeros((len(batch_size), len(percent_positive)))
data_missed = np.zeros((len(batch_size), len(percent_positive)))
data_extra = np.zeros((len(batch_size), len(percent_positive)))

false_pos = 0.1 #10% likelihood of false positives
false_neg = 0.1 #10% likelihood of false negatives


for bs,k in enumerate(batch_size):
    number_of_batches = int(Num_of_tests / k)
    
    leftovers = Num_of_tests % k #We'll have to add these in at the end as individual tests.
    #print(number_of_batches, number_of_batches*k,int(number_of_batches*k+leftovers))
    for ind, pos in enumerate(percent_positive):
        #likelihood of negative batch test:
        neg_result = (1-pos/100)**k
        #likelihood of positive test:
        pos_result = 1 - neg_result
        #Expectated number of tests per batch
        tests_per_batch = 1 + k * pos_result
        tests_per_batch_with_false = 1 + (1-false_neg)*k * pos_result + k * false_pos * neg_result
        total = number_of_batches *(tests_per_batch) + leftovers
        total_with_false = number_of_batches * tests_per_batch_with_false + leftovers
        total_missed = number_of_batches * false_neg * k * pos_result
        total_extra = number_of_batches * false_pos * k * neg_result
        data_array[bs][ind] = ceil(total)/ Num_of_tests
        data_array_with_false[bs][ind]= ceil(total_with_false) / Num_of_tests
        data_missed[bs][ind] = ceil(total_missed) / Num_of_tests
        data_extra[bs][ind] = ceil(total_extra) / Num_of_tests                   



d1 = data_array[2,:]
d2 = data_array_with_false[2,:]
d3 = data_missed[2,:]
d4 = data_extra[2,:]
x = percent_positive
plt.plot(x,d1,x,d2,x,d3,x,d4)
leg=['Perfect Accuracy', 'Total Tests with False Pos/Neg', 'Total Retests Missed', 'Total Unneccesary Retests']
plt.legend(leg,loc='upper center')
plt.xlabel('True Percent Postive Rate', fontsize=14)
plt.ylabel('Normalized Tests', fontsize=14)
plt.suptitle('Testing with 10% False Postives and Negatives\nand a Batch Size of 4', fontsize=16)
plt.ylim(0,1)

    