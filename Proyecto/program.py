#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 23:26:28 2018

@author: Ghost
"""
import random
import functions
import objects

#------------- Importando y limpiando demanda  ------------------------
demand = functions.getDemandList('data/demanda2018Ciclo2.xlsx', 'Hoja2')
#print functions.letJustDepartmentDemand(demand)

#-------------Agregar para n planes----------
dataPlanM2016 = functions.getDataList('data/planM2016.csv')
dataPlanE2016 = functions.getDataList('data/planE2016.csv')
#Talvez agregar Plan Viejo M
#Talvez agregar plan Viejo E


 #------------- Creando Objetos de los cursos para el semestre en funcion de la demanda ----------

allCourses = functions.mergeAllCourses([dataPlanE2016, dataPlanM2016,], 
                                        functions.letJustDepartmentDemand(demand))
#print allCourses                                    
#for i in range(len(allCourses)): print allCourses[i].code #Ver cursos a programar
                                        
#------------- Importando profesores ------------------------

allTeachers = functions.readTeachers('data/profesores.xlsx')
#for i in range(len(allTeachers)):
    #print allTeachers[i].name
    #print allTeachers[i].workTime

#print allTeachers[0].workTime[0]

#--- Verify Av. -----

[ verify , error] = functions.verifyTeacherAv(allTeachers, allCourses)
print verify
print error