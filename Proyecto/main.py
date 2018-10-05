#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 23:15:28 2018

@author: Ghost
"""
from extractData import generateData
from initialize import initialize
from geneticAlgorithm import geneticAlgorithm as GA

from selection import generate_selection
from fitness import generate_fitness
from mutation import generate_mutation
from crossover import crossover

from functions import showCompleteData as sortData
from functions import logger
from functions import generate_exitDataToExcel
from functions import saveData
from functions import printProcess
import numpy as np

# ---- VARIABLES OF THE ALGORYTHM -------------
poblation = 50000
maxGenerations = 1000
initializeLogger = 1000
# Selection parameters
OUTSTANDING_PERCENTAGE = 0.35
MAX_PAIRS = 300
#Mutation parameters
probability = 0.01
# -------------------------------------
#print parameters
printFrequency = 20
writeData = True
writeProcess = False
#---------------------
write_Year_Excel = True
write_Teacher_Excel = True
write_Lab_Excel = True
#----------------------
# Importando Datos de Excel ---------------------
allPeriods,allLabs,allTeachers,forbiddenTime,theoryCheck,labCheck = generateData(poblation)
# -----------------------------------------------
#print len(allPeriods)
print theoryCheck
print labCheck
print ""



#Inicializando Periodos(generación) con datos de Periodo, Dia y Profesor
g0 = initialize(allPeriods,allLabs,allTeachers, poblation, initializeLogger)


genetic_scheduling = GA(
    g0,
    generate_selection(OUTSTANDING_PERCENTAGE,MAX_PAIRS),
    generate_fitness(allLabs, allTeachers, forbiddenTime),
    crossover,
    generate_mutation(probability, allLabs, allTeachers, forbiddenTime),
    maxGenerations,
    logger,
    generate_exitDataToExcel(allLabs, forbiddenTime, allTeachers ,write_Lab_Excel,write_Teacher_Excel,write_Year_Excel ,printFrequency),
    saveData(writeData),
    printProcess(writeProcess)
)

bestIndividual = genetic_scheduling.optimize()

#bestIndividual, writeLabs, writeTeachers, writeYear
#exitDataToExcel(bestIndividual['individual'],allLabs, forbiddenTime, allTeachers ,True,True,True,printFrequency)
#
# print
# for time in forbiddenTime:
#     print
#     print time.prettyForbiddenTime

print sortData(bestIndividual['individual'])
# scores = fitness(bestParentsList)
#
# #Show Best Parent
# ind = np.argmax(scores)
# print "PUNTUACIÓN: "+str(scores[ind])
#
# bestParent = bestParentsList[0][ind]
#
# print sortData(bestParent)
