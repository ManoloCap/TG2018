#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 23:15:28 2018

@author: Ghost
"""
from extractData import generateData as generateData
from initialize import initialize as initialize
from geneticAlgorithm import geneticAlgorithm as GA

from selection import selection as selection
from fitness import fitness as fitness
from mutation import mutation as mutation
from crossover import crossover as crossover

from functions import showCompleteData as sortData
import numpy as np
# ---- VARIABLES OF THE ALGORYTHM -------------
poblation = 4
goodValue = 90000
# -------------------------------------

# Importando Datos de Excel ---------------------
allPeriods,allLabs,allTeachers,forbiddenTime,theoryCheck,labCheck = generateData(poblation)
# -----------------------------------------------
#print len(allPeriods)
print theoryCheck
print labCheck
print ""

#Inicializando Periodos(generación) con datos de Periodo, Dia y Profesor
generation = initialize(allPeriods,allLabs,allTeachers)

g0 = [generation, allLabs, allTeachers, forbiddenTime]

#fitness(g0)
genetic_scheduling = GA(
    g0,
    selection,
    fitness,
    crossover,
    mutation,
    goodValue
)

bestParents = genetic_scheduling.optimize()


#terminando para mostrar
scores = fitness(bestParents)

#Show Best Parent
ind = np.argmax(scores)
print "PUNTUACIÓN: "+str(scores[ind])

bestParent = bestParents[0][ind]

print sortData(bestParent)
