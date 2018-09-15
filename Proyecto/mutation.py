#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def mutation(candidate):
    # TODO: return new candidate
    #cantidad de mutaciones máximas
    maxMutations = 300

    #Mutaciones reales
    mutations = random.randrange(0, maxMutations, 1)
    #--------------------------

    [parents, allLabs, allTeachers, forbiddenTime]  = candidate

    for period in range(len(parents)):
        mutations = random.randrange(0, maxMutations, 1)
        #print "MUTACIONES: "+str(mutations)
        for x in range(mutations):
            mutationType = random.randrange(0,4,1)

            if(mutationType == 0): #Mutacion de día
                newDay = random.randrange(0,5,1)
                parents[period].day = newDay

            elif(mutationType == 1): #Mutación de Periodo
                newPeriod = random.randrange(0,17,1)
                parents[period].period = newPeriod

            elif(mutationType == 2): #Mutacion de teacher
                newTeacher = random.choice(allTeachers.keys())
                parents[period].section.teacher = newTeacher

            elif(mutationType == 3): #Mutación de número de laboratorio
                newPeriod = random.randrange(0, len(allLabs), 1)
                parents[period].section.labNumber = newPeriod


    return [parents, allLabs, allTeachers, forbiddenTime]
