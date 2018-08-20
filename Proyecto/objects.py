#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 22:25:26 2018

@author: Ghost
"""

class course:
    
    def __init__(self,year,cicle,code,theoryPeriods,labPeriods,cred,name,pensum, demand, sections):
        
        self.year = year
        self.cicle = cicle
        self.code = code
        self.theoryPeriods = theoryPeriods
        self.labPeriods = labPeriods
        self.cred = cred
        self.name = name
        self.pensum = pensum
        self.demand = demand
        self.sections = sections


class teacher:
    
    def __init__(self,name, workTime, theoryPeriods, labPeriods):
        
        self.name = name
        self.workTime = workTime
        self.theoryPeriods = theoryPeriods
        self.labPeriods = labPeriods
        
class forbiddenTime:
    def __init__(self, year, forbiddenTime):
        self.year = year
        self.forbiddenTime = forbiddenTime
        
class section:
    def __init__(self,course, teacher, position, classType, code):
        self.course = course
        self.teacher = teacher
        self.postition = position # 'DPPP..Pn' , 'DPPP...Pn', ..... n
        self.classType = classType # LAB or TH
        self.laboratory = None
        self.code = code

class laboratory: #ClassRoom
    
    def __init__(self,number):
       
        laboratoryT = []
        row = []
        for i in range(17):
            for j in range(5):
                row.append('x')
            laboratoryT.append(row)
            row = []
 
        self.time = laboratoryT
        self.number = number
