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

    def __init__(self,name, workTime, theoryPeriods, labPeriods,coursesList, prettyWorkTime, usedTime, demandLeft):

        self.name = name
        self.workTime = workTime
        self.theoryPeriods = theoryPeriods
        self.labPeriods = labPeriods
        self.coursesList = coursesList
        self.prettyWorkTime = prettyWorkTime
        self.usedTime = usedTime
        self.demandAssigned = { 'LAB' : {} , 'TH' : {} }
        self.demandLeft = demandLeft
        self.sections = []

class forbiddenTime:
    def __init__(self, year, forbiddenTime, prettyForbiddenTime):
        self.year = year
        self.forbiddenTime = forbiddenTime
        self.prettyForbiddenTime = prettyForbiddenTime

class section:
    def __init__(self,course, teacher, position, classType, code):
        self.course = course
        self.teacher = teacher
        self.postition = position # 'DPPP..Pn' , 'DPPP...Pn', ..... n
        self.classType = classType # LAB or TH
        self.code = code
        self.labNumber = ''

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
        self.prettyUsedTime = []

class period:

     def __init__(self, section, period, day, teacher, code):

        self.section = section
        self.period = period
        self.day = day
        self.teacher = teacher
        self.code = code
