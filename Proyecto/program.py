#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 23:26:28 2018

@author: Ghost
"""
#import random
import functions
import objects
from pprint import pprint

#------------- NUMERO DE LABORATORIOS  ------------------------
labs= 2
allLabs = {}
for i in range(labs):
    bufferLab = objects.laboratory(i)
    allLabs.update( { bufferLab.number + 1 : bufferLab})

#print allLabs
#------------- Importando y limpiando demanda  ------------------------
demand = functions.getDemandList('data/demanda2018Ciclo2.xlsx', 'Hoja2')
#print functions.letJustDepartmentDemand(demand)

#-------------Agregar para n planes----------
dataPlanM2016 = functions.getDataList('data/planM2016.csv')
dataPlanE2016 = functions.getDataList('data/planE2016.csv')
#Talvez agregar Plan Viejo M
#Talvez agregar plan Viejo E


 #------------- Creando Objetos de los cursos para el semestre en funcion de la demanda ----------
maxTheory = 30  # Numero maximo de estudiantes por seccion
maxLeftOver = 3 # Numero maximo de estudiantes que pueden quedar de mas aparte de los 15 por seccion antes de abrir una nueva

allCourses = functions.mergeAllCourses([dataPlanE2016, dataPlanM2016,], 
                                        functions.letJustDepartmentDemand(demand),
                                        maxTheory,
                                        maxLeftOver)
#print allCourses                                    
#for i in range(len(allCourses)): print allCourses[i].code #Ver cursos a programar
                                        
#------------- Importando profesores ------------------------

allTeachers = functions.readTeachers('data/profesores.xlsx')
#for i in range(len(allTeachers)):
    #print allTeachers[i].name
    #print allTeachers[i].workTime

#print allTeachers[0].workTime[0]

#--------------------------- Verify Av. -------------------------

[ verify , error] = functions.verifyTeacherAv(allTeachers, allCourses)
#print verify
#print error



# ----------------- Adding forbiddenTime ---------------------------
forbiddenTime = functions.loadForbiddens('data/horariosProhibidos.xlsx')

#for i in range(len(forbiddenTime)):
#    pprint(forbiddenTime[i])



# --------------  PARTE ASIGNACIÓN DE HORARIOS -------------------

labMax = 15
labLeftOver =  4
allSections = functions.InitialSolution(allCourses, labMax, labLeftOver)


# Contador secciones para cada curso dentro del vector solución
contadorSeccionesTH = {}
contadorSeccionesLAB = {}

for i in range(len(allSections)):
    if(allSections[i].course.code in contadorSeccionesLAB or allSections[i].course.code in contadorSeccionesTH ):
        
        if(allSections[i].classType == 'TH'):
            contadorSeccionesTH.update( { allSections[i].course.code : contadorSeccionesTH[allSections[i].course.code] + 1 } )
        elif(allSections[i].classType == 'LAB'):
            contadorSeccionesLAB.update( { allSections[i].course.code : contadorSeccionesLAB[allSections[i].course.code] + 1 } )

    else:
        if(allSections[i].classType == 'TH'):
            contadorSeccionesTH.update( { allSections[i].course.code : 1 } )
            
            if(int(allSections[i].course.labPeriods) != 0):
                contadorSeccionesLAB.update( { allSections[i].course.code : 0 } )
                
        elif(allSections[i].classType == 'LAB'):
            contadorSeccionesLAB.update( { allSections[i].course.code : 1 } )
            
            if(int(allSections[i].course.theoryPeriods) != 0):
                contadorSeccionesTH.update( { allSections[i].course.code : 0 } )
                
            
#   mostrar contadores  
print contadorSeccionesTH
print contadorSeccionesLAB
print len(allSections)
for i in range(len(allSections)):
    print allSections[i].code     



#print len(periodCounter)
#print allCourses['IE2008'].labPeriods
#print ""
#
#print teoriaCounter
#print labCounter
#--------------------------------------------------------------------

#print len(allSections)
#Asignando posciciones iniciales
#print allTeachers[u'Miguelnose_apellidoapellido2'].workTime

    
allSections, allTeachers, allLabs, errorSections = functions.assignInitial(allSections, allCourses, allTeachers, allLabs)

# Show Teachers Space

# for key in allTeachers:
#     print key
#     print ""
#     for i in range(len(allTeachers[key].workTime)):
#          print allTeachers[key].workTime[i]
#     print ""
# 


# show laboratory Space

# for i in range(len(errorSections)):
#     print errorSections[i].course.code
# 
# for key in allLabs:
#     print ""
#     for i in range(len(allLabs[key].time)):
#         print allLabs[key].time[i]
#     print ""
#

# Show Sections

#for i in range(len(allSections)):
#    pprint(allSections[i])
