# Covid_batch_size
Plots of optimal batch sizes based on number of positive results

<b>TL;DR</b>: Python code that calculates optimal batch size based on percent positive, and percent positive based on batch results.  Results: A batch size of 4 or 5 is optimal for 6-10% positive rate (about what the US has right now).  Using batch processing can reduce the number of requied tests by 50-60%.

The basic idea is to calculate how many total tests must be performed.  This information can be used to optimize scarce resources.

Note: There is a distinction between a <b>sample</b> and a <b>test</b>.  A <b>sample</b> is a collection from an individual.  A <b>test</b> is the actual determination of positive or negative for a sample or for a batch (a group of samples).  If a batch is tested and the result is negative, that means that all individual samples in the batch are negative.  If the batch is positive, there is at least one positive sample in the batch.  All samples in the batch must then be tested individually.  

This program attempts to figure out the optimal batch size for testing.

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

Note: The results from the file are normalized by the number of tests performed.  
