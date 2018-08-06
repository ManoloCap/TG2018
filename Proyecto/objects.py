#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 22:25:26 2018

@author: Ghost
"""

class course:
    
    def __init__(self,year,cicle,code,theoryPeriods,labPeriods,cred,name,pensum):
        
        self.year = year
        self.cicle = cicle
        self.code = code
        self.theoryPeriods = theoryPeriods
        self.labPeriods = labPeriods
        self.cred = cred
        self.name = name
        self.pensum = pensum

class teacher:
    
    def __init__(self,name, workTime, theoryPeriods, labPeriods):
        
        self.name = name
        self.workTime = workTime
        self.theoryPeriods = theoryPeriods
        self.labPeriods = labPeriods
        