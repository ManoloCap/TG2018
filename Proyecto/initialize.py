#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from objects import period

def initialize(allPeriods,allLabs,allTeachers):
    generation = []
    for parent in range(len(allPeriods)):
        generation.append([])
        for section in range(len(allPeriods[parent])):

            # Variables random para inicializar
            randomLab = random.randrange(0,len(allLabs[parent]),1)
            randomTeacher = random.choice(allTeachers[parent].keys())
            randomPeriod = random.randrange(0,17,1)
            randomDay = random.randrange(0,5,1)

            # Actualizando teacher en la sección
            allPeriods[parent][section][allPeriods[parent][section].keys()[0]].teacher = randomTeacher
            # actualizando Variable en sección en caso de ser Laboratorio
            if(allPeriods[parent][section][allPeriods[parent][section].keys()[0]].classType == 'LAB'):
                allPeriods[parent][section][allPeriods[parent][section].keys()[0]].labNumber = randomLab

            #Creando Periodos
            new_Period = period( allPeriods[parent][section][allPeriods[parent][section].keys()[0]],
                        randomPeriod,
                        randomDay)
            generation[parent].append(new_Period)


    # print "GEN LEN: "+str(len(generation))
    return generation
