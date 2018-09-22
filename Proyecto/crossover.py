#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from objects import period as createPeriod
def crossover(parent1, parent2):
    # TODO: return array of new candidates

    # Recombinación de un punto (LA MTIAD) -------
    # punto = len(parent1) / 2
    # bufferParent = []
    # for i in range(punto):
    #
    #     bufferParent.append(parent1[i])
    #
    #
    # for i in range(punto,len(parent2),1):
    #
    #     bufferParent.append(parent2[i])

    # Recombinación de un punto (random) -------
    punto = random.randrange(0, len(parent1),1)
    parentList = [ parent1, parent2 ]

    bufferParent = []
    for i in range(punto):
        #print i
        bufferParent.append(parent1[i])


    for i in range(punto,len(parent2),1):
        #print i
        bufferParent.append(parent2[i])


    # # Recombinación random ------ ------------------------ -----------
    #
    # parentList = [ parent1, parent2 ]
    #
    #
    # bufferParent = []
    # for i in range(len(parent2)):
    #     #print i
    #     randomParent = random.randrange(0,2,1)
    #     randomParent = parentList[randomParent]
    #     bufferParent.append(randomParent[i])
    #
    #
    #
    # # --------------------------------------------------------------


    # Creacion de nuevos objetos tipo periodo
    child = []
    for actualPeriod in bufferParent:
        new_Period = createPeriod( actualPeriod.section,
                    actualPeriod.period,
                    actualPeriod.day,
                    actualPeriod.teacher,
                    actualPeriod.code)
        child.append(new_Period)

    return [parent1, parent2, child]
