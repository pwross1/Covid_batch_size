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
        total = number_of_batches *(tests_per_batch) + leftovers
#        print('Neg: {:.2f}, Pos:{:.2f}, batch: {:d}, tests_per:{:.3f}, total:{:d}'.format(neg_result, pos_result, k, tests_per_batch, int(total)))
#        print('For a batch size of {} and a percent positive of {}, the total is {}'.format(k, pos, ceil(total)))
        data_array[bs][ind] = ceil(total)/ Num_of_tests


for ind,k in enumerate(batch_size):
    x = percent_positive
    y = data_array[ind][:]
    leg.append('{} per batch'.format(k))
    plt.plot(x,y)
    plt.legend(leg,title='Tests per Batch',loc='lower right')
    plt.xlabel('Percent Postive Rate', fontsize=14)
    plt.ylabel('Normalized Total Tests', fontsize=14)
    plt.suptitle('Total Tests for Different Batch Sizes', fontsize=20)
    plt.ylim(0,0.8)
    

fig2, ax2=plt.subplots()

for ind, pos in enumerate(percent_positive):
    x = batch_size
    y = data_array[:,ind]
    leg2.append('{}% positive'.format(pos))
    ax2.plot(x,y, label ='{}%'.format(pos) )
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles[::-1], labels[::-1], title = 'Positive Rate',loc='center right')
    plt.xlabel('Batch Size', fontsize=14)
    plt.ylabel('Normalized Total Tests', fontsize=14)
    plt.suptitle('Total Tests for Different Positive Rates', fontsize=18)
    plt.ylim(0,1)
    plt.xlim(1,14)