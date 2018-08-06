#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 20:14:11 2018

@author: Ghost
"""
import pandas as pd
import numpy as np
import objects
import math

cursos = {}

def getDemandList(route, sheet):
    df = pd.read_excel(route,  sheetname=sheet)
    data = df.values.tolist()
    #data = transpuesta(data)
    return data

def letJustDepartmentDemand(demand):
    #IN: Type: List of Demand
    bufferDic = {}
    for i in range(len(demand)):
        try:
            if(str(demand[i][0])[0:2] == u"IE" or str(demand[i][0])[0:2] == u"MM"):
                actualDemandDic = { demand[i][0] : int(math.ceil(demand[i][4])) }
                bufferDic.update(actualDemandDic)
        except UnicodeEncodeError:
            None
    #OUT: type: DIC - { Code : student_Demand }
    return bufferDic

def print_r(matriz):
    for fila in matriz:
        print fila

def transpuesta(matriz):
    rows = len(matriz)
    cols = len(matriz[0])
    return [[matriz[j][i] for j in xrange(rows)] for i in xrange(cols)]
    

def getDataList(route):
    df = pd.read_csv(route)
    data = df.values.tolist()
    data = transpuesta(data)
    return data
    

    
def createListOfObjects(dataPlan, pensum):
    listOfObjects = []
    for index in range(len(dataPlan[0])):
        newObject = objects.course(dataPlan[13][index], dataPlan[15][index], dataPlan[16][index], str(dataPlan[17][index])[0], str(dataPlan[17][index])[1], str(dataPlan[17][index])[2], dataPlan[20][index], pensum)
        listOfObjects.append(newObject)
    
    #OUT: List of Objects "Course"
    return listOfObjects

def mergeAllCourses(dataPlanList, demand):
    objectCoursesList = []
    for i in range(len(dataPlanList)):
        objectCoursesList.append(createListOfObjects(dataPlanList[i], i))
      
    for i in range(len(objectCoursesList)-1):
        objectCoursesList[0].extend(objectCoursesList[i+1])
    

    for e in range(len(objectCoursesList[0])):
        for i in range(len(objectCoursesList[0])):
            try:
                if(objectCoursesList[0][e].code == objectCoursesList[0][i].code and
                   e != i):
                    objectCoursesList[0][i] = None
            except AttributeError:
                None
                #print( str(counter)+" -- "+str(i))

    departmentList = []
    exitData = {}
    for i in range(len(objectCoursesList[0])):
        try:
            objectCoursesList[0][i].code
            if(str(objectCoursesList[0][i].code) == 'nan'):
                None
            
            if(str(objectCoursesList[0][i].code)[0:2] == 'IE' or
               str(objectCoursesList[0][i].code)[0:2] == 'MM'):
                departmentList.append(objectCoursesList[0][i])
        except AttributeError:
            None
            
    for i in range(len(departmentList)):
        if(departmentList[i].code in demand):
            exitData.update({ departmentList[i].code : departmentList[i] })
    
    return exitData

def verifyTeacherAv(listOfTeachers, listOfCourses):
    exitData = []
    error = None
    for t in range(len(listOfTeachers)):
        #print listOfTeachers[t].labPeriods
    #for t in range(len(listOfTeachers)):
        totalPeriods = 0
        for i in range(len(listOfTeachers[t].workTime)):

            for j in range(len(listOfTeachers[t].workTime[i])):
                #print listOfTeachers[t].workTime[i][j]
                if(listOfTeachers[t].workTime[i][j] == "x"):
                    #print listOfTeachers[t].workTime[i][j]
                    totalPeriods = totalPeriods+1
                    #print "sumando"
                    None
        periodsCount = 0
        for key in listOfTeachers[t].theoryPeriods:
            try:
                periodsCount = periodsCount + int(listOfCourses[key].theoryPeriods)*int(listOfTeachers[t].theoryPeriods[key])
            except KeyError:
                error = "ERROR: El profesor "+listOfTeachers[t].name+" tiene asignado un curso que no corresponde a la demanda"
                break
            
        for key in listOfTeachers[t].labPeriods:
            try:
                periodsCount = periodsCount + int(listOfCourses[key].labPeriods)*int(listOfTeachers[t].labPeriods[key])
            except KeyError:
                error = "ERROR: El profesor "+listOfTeachers[t].name+" tiene asignado un curso que no corresponde a la demanda"
                break

        if(periodsCount > totalPeriods):
            error = "ERROR: El profesor "+listOfTeachers[t].name+u" Tiene asignados más periodos que espacio de trabajo"

    #print listOfTeachers[0].workTime
        exitBuffer = { listOfTeachers[t].name : [periodsCount, totalPeriods] }
        exitData.append(exitBuffer)
    return [exitData , error ]
    
def readTeachers(route):
    xls = pd.ExcelFile(route)
    teacherList = []
    for indexProfesor in range(len(xls.sheet_names)):
        actualTeacher = pd.read_excel(route, xls.sheet_names[indexProfesor])
        actualTeacher = actualTeacher.values.tolist()
        name = actualTeacher[0][4].replace(" ", "")+"_"+actualTeacher[1][4].replace(" ", "")
        workTime = actualTeacher[3:21]
        workMatrix = []
        theoryPeriods = {}
        labPeriods = {}
        for i in range(len(workTime)):
            if(i == 4):
                None
            else:
                workMatrix.append(workTime[i][3:8])
            if(str(workTime[i][8]) != 'nan'):
                bufferDic = { workTime[i][8]:workTime[i][9] }
                theoryPeriods.update(bufferDic)
                bufferDic = { workTime[i][8]:workTime[i][10] }
                labPeriods.update(bufferDic)
            
        teacherList.append(objects.teacher( name, workMatrix, theoryPeriods, labPeriods))  
    #data = transpuesta(data)
   
    #print teacherData[0][4]
    return teacherList