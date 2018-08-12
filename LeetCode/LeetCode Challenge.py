# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 16:06:10 2018

@author: jkoeh
"""

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        numDict ={}  
        for index in range(len(nums)):            
            compliment = target - nums[index]                
            if(compliment in numDict):
                return [numDict[compliment], index]
            else:
                numDict[nums[index]] = index
        raise ValueError
        