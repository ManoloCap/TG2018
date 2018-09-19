#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from objects import period

def initialize(allPeriods,allLabs,allTeachers,poblation, loggerVar):

    generation = []
    for parent in range(poblation):
        if parent % loggerVar == 2 : print parent
        new_Parent = []
        for section in range(len(allPeriods)):
            # Variables random para inicializar
            randomLab = random.randrange(0,len(allLabs),1)
            randomTeacher = random.choice(allTeachers.keys())
            randomPeriod = random.randrange(0,17,1)
            randomDay = random.randrange(0,5,1)

            # Actualizando teacher en la sección
            allPeriods[section][allPeriods[section].keys()[0]].teacher = randomTeacher
            # actualizando Variable en sección en caso de ser Laboratorio
            if(allPeriods[section][allPeriods[section].keys()[0]].classType == 'LAB'):
                allPeriods[section][allPeriods[section].keys()[0]].labNumber = randomLab

            #Creando Periodos
            new_Period = period( allPeriods[section][allPeriods[section].keys()[0]],
                        randomPeriod,
                        randomDay,
                        allPeriods[section][allPeriods[section].keys()[0]].teacher,
                        allPeriods[section][allPeriods[section].keys()[0]].code)
            new_Parent.append(new_Period)

        generation.append(new_Parent)

    print "GEN LEN: "+str(len(generation))
    return generation
