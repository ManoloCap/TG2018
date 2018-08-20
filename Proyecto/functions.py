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
import random

class GetOutOfLoop( Exception ):
    pass


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
            if(str(demand[i][0])[0:2] == u"IE" or str(demand[i][0])[0:2] == u"IM"):
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
        
        newObject = objects.course(dataPlan[13][index], dataPlan[15][index], dataPlan[16][index], str(dataPlan[17][index])[0], str(dataPlan[17][index])[1], str(dataPlan[17][index])[2], dataPlan[20][index], pensum, 0, 0)
        listOfObjects.append(newObject)
    
    #OUT: List of Objects "Course"
    return listOfObjects

def mergeAllCourses(dataPlanList, demand, maxTheory, maxLeftOver):
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
               str(objectCoursesList[0][i].code)[0:2] == 'MT'):
                departmentList.append(objectCoursesList[0][i])
        except AttributeError:
            None
        
    for i in range(len(departmentList)):
        #Llenando demanda; y cantidad de secciones que necesitara el curso en funcion del numero de maximo para teoria y demanda de estudiantes
        if(departmentList[i].code in demand):
            departmentList[i].demand = demand[departmentList[i].code]
            departmentList[i].sections = departmentList[i].demand/maxTheory
            if(departmentList[i].demand % maxTheory > maxLeftOver):
                departmentList[i].sections = departmentList[i].sections + 1
            #print departmentList[i].sections
            exitData.update({ departmentList[i].code : departmentList[i] })
            #print departmentList[i].theoryPeriods
    
    return exitData

def verifyTeacherAv(listOfTeachers, listOfCourses):
    exitData = []
    error = None
    listOfTeachers2 = listOfTeachers
    listOfTeachers = []
    for key in listOfTeachers2:
        listOfTeachers.append(listOfTeachers2[key])
        
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
    teacherList = {}
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
            
        teacherList.update({ name : objects.teacher( name, workMatrix, theoryPeriods, labPeriods)})
    #data = transpuesta(data)
   
    #print teacherData[0][4]
    return teacherList

def loadForbiddens(route):
    xls = pd.ExcelFile(route)
    forbiddenList = []
    for indexYear in range(len(xls.sheet_names)):
        actualYear = pd.read_excel(route, xls.sheet_names[indexYear])
        
        actualYear = actualYear.values.tolist()
        workTime = actualYear[3:21]
        workMatrix = []
        #print workTime
        for i in range(len(workTime)):
            if(i == 4):
                None
            else:
                workMatrix.append(workTime[i][3:8])
                
        
        forbiddenList.append(objects.forbiddenTime(xls.sheet_names[indexYear], workMatrix))
        #print objects.forbiddenTime(xls.sheet_names[indexYear], workMatrix)
        #forbiddenList.append(objects.forbiddenTime( year, forbiddenPeriods))  
    #data = transpuesta(data)
   
    #print teacherData[0][4]   
    return forbiddenList
    
#FITNESS_COURSES (First for years)
def FITNESS_COURSES(solution, allCourses, allTeachers, forbiddenTime):
    # Puntaje para cada uno

    return None
    
def InitialSolution(allCourses, labMax, labLeftOver):
    labSections = 0
    allSections = []
    contadorSecciones = 0
    contadorSeccioensLab = 0
    
    for key in allCourses:
        #print key+"  "+str(allCourses[key].demand)
        for s in range(allCourses[key].sections):
            
            allSections.append(objects.section(allCourses[key], None, None, 'TH', str(s+1)+'0'+key))
            #print  str(s+1)+'0'+key+' TH'
            #print key+"  "+'TH'
            contadorSecciones = contadorSecciones + 1
            
            #print str(s+1)+'0'+key
            
        if(int(allCourses[key].labPeriods) != 0):
            #print allCourses[key].labPeriods
            
            if(allCourses[key].demand % labMax > labLeftOver):
                labSections = allCourses[key].demand/labMax + 1
            else:
                labSections = allCourses[key].demand/labMax
                
            #print labSections
            labSection = 1
            contador = 1
            for l in range(labSections):
                if(contador == 2):
                    
                    allSections.append(objects.section(allCourses[key], None, None, 'LAB', str(labSection)+str(contador)+key))
                    #print ""                    
                    #print str(labSection)+str(contador)+key+' LAB'
                    #print key+"  "+'LAB'
                    contadorSeccioensLab = contadorSeccioensLab +1
                    contador = 1
                    labSection = labSection +1
                    
                else:
                    allSections.append(objects.section(allCourses[key], None, None, 'LAB', str(labSection)+str(contador)+key))
                    #print str(labSection)+str(contador)+key+' LAB'
                    contador = contador + 1
                    
                
                
    
    return allSections

def putPosition(section, allSections, allTeachers, allLabs):
    status = 'FAIL'
    #print section.course.code
    try:
        if(section.classType == 'TH'):
            periods = int(section.course.theoryPeriods)
            
            for key in allTeachers:
                if( section.course.code in allTeachers[key].theoryPeriods):
                    for F in range(len(allTeachers[key].workTime)):
                        for C in range(len(allTeachers[key].workTime[F])):
                            
                            if(allTeachers[key].workTime[F][C] == 'x' and ((F+periods-1) < 17 )):
                                #print periods
                                if(periods < 4 and
                                   allTeachers[key].workTime[F+1][C] == 'x' and
                                   allTeachers[key].workTime[F+2][C] == 'x' and 
                                   allLabs):
                                       
                                       allTeachers[key].workTime[F][C] = section.course.code
                                       allTeachers[key].workTime[F+1][C] = section.course.code
                                       allTeachers[key].workTime[F+2][C] = section.course.code
                                       section.teacher = allTeachers[key]
                                       section.position = str(C)+str(F)+str(F+1)+str(F+2)
                                       #for i in range(len(allTeachers[key].workTime)):
                                           #print allTeachers[key].workTime[i]
                                       #print ""
                                       
                                       status = 'SUCCESS'
                                       raise GetOutOfLoop
                                       
                                    
                                    
                    
        elif(section.classType == 'LAB'):
            periods = int(section.course.labPeriods)
    
            for key in allTeachers:
                if( section.course.code in allTeachers[key].labPeriods):
                    for F in range(len(allTeachers[key].workTime)):
                        for C in range(len(allTeachers[key].workTime[F])):
                            if(allTeachers[key].workTime[F][C] == 'x' and ((F+periods-1) < 17 )):
                                #print periods
                                if(periods < 4 and
                                   allTeachers[key].workTime[F+1][C] == 'x' and
                                   allTeachers[key].workTime[F+2][C] == 'x'):
                                       
                                       for labKey in allLabs:
                                           
                                           if(allLabs[labKey].time[F][C] == 'x' and
                                              allLabs[labKey].time[F+1][C] == 'x' and
                                              allLabs[labKey].time[F+2][C] == 'x'):
                                                  
                                               #SETTING TEACHERS TIME
                                               allTeachers[key].workTime[F][C] = section.course.code
                                               allTeachers[key].workTime[F+1][C] = section.course.code
                                               allTeachers[key].workTime[F+2][C] = section.course.code
                                               
                                               #SETTING SECTION TIME
                                               section.teacher = allTeachers[key]
                                               section.position = str(C)+str(F)+str(F+1)+str(F+2)
                                               #for i in range(len(allTeachers[key].workTime)):
                                                   #print allTeachers[key].workTime[i]
                                               #print ""
                                               
                                               # SETTING LAB TIME
                                               allLabs[labKey].time[F][C] = section.course.code
                                               allLabs[labKey].time[F+1][C] = section.course.code
                                               allLabs[labKey].time[F+2][C] = section.course.code
                                               status = 'SUCCESS'
                                               raise GetOutOfLoop

        
    except GetOutOfLoop:
        pass   

    return allSections, allTeachers, allLabs, status
        
def assignInitial(allSections, allCourses, allTeachers, allLabs):
    successCount = 0
    errorSections = []
    for i in range(len(allSections)):
        allSections, allTeachers, allLabs, status = putPosition(allSections[i], allSections, allTeachers, allLabs)
        
        if( status == 'SUCCESS' ):
            successCount = successCount + 1
        else:
            errorSections.append(allSections[i])
            #print allSections[i].teacher.name
        #print allSections[i].course.code
        #print str(i)+" "+status
        #print ""
    print str(successCount)+" of "+str(len(allSections))    
    return allSections, allTeachers, allLabs, errorSections