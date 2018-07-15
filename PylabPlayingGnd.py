# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 14:22:37 2018

@author: Johann
"""

import pylab as plt
mysamples = []
mylinear = []
myquadratic = []

for i in range(0, 30):
    mysamples.append(i)
    mylinear.append(i+1)
    myquadratic.append(i**2)
plt.figure('linquad')
plt.clf()
plt.plot(mysamples, mylinear, label = 'linear')
plt.plot(mysamples, myquadratic, label = 'quad')
plt.yscale('log')
plt.legend()
plt.title('Linear vs Quad')