# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 07:52:21 2018

@author: Johann
"""

import random
def rollDie():
    return random.choice([1,2,3,4,5,6])
def genEven():
    '''
    Returns a random even number x, where 0 <= x < 100
    '''
    return random.choice(range(0, 100, 2))

def testRoll(n=100):
    for i in range(n):        
        print(random.randrange(0, 10))
    

print((1/2*3/5*2/4+1/2*2/5*3/4+1/2*3/5*2/4).as_integer_ratio())