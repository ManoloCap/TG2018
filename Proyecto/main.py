#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 23:15:28 2018

@author: Ghost
"""
from extractData import generateData
from initialize import initialize
from geneticAlgorithm import geneticAlgorithm as GA

from selection import selection
from fitness import generate_fitness
from mutation import generate_mutation
from crossover import crossover

from functions import showCompleteData as sortData
from functions import logger
from functions import exitDataToExcel
import numpy as np

# ---- VARIABLES OF THE ALGORYTHM -------------
poblation = 1000
maxGenerations = 50
initializeLogger = 200
# -------------------------------------

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
    selection,
    generate_fitness(allLabs, allTeachers, forbiddenTime),
    crossover,
    generate_mutation(allLabs, allTeachers, forbiddenTime),
    maxGenerations,
    logger
)

bestIndividual = genetic_scheduling.optimize()

#bestIndividual, writeLabs, writeTeachers, writeYear
exitDataToExcel(bestIndividual['individual'],allLabs, forbiddenTime, allTeachers ,True,True,True)

# scores = fitness(bestParentsList)
#
# #Show Best Parent
# ind = np.argmax(scores)
# print "PUNTUACIÓN: "+str(scores[ind])
#
# bestParent = bestParentsList[0][ind]
#
# print sortData(bestParent)
