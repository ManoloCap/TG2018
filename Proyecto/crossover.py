#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from objects import period as createPeriod
def crossover(parent1, parent2):
    # TODO: return array of new candidates

    # # Recombinación de un punto (LA MTIAD) -------
    # punto = len(parent1) / 2
    # bufferParent = []
    # for i in range(punto):
    #
    #     bufferParent.append(parent1[0][i])
    #
    #
    # for i in range(punto,len(parent2[0]),1):
    #
    #     bufferParent.append(parent2[0][i])

    # Recombinación de un punto (random) -------
    punto = random.randrange(0, len(parent1[0]),1)
    parentList = [ parent1, parent2 ]

    bufferParent = []
    for i in range(punto):
        #print i
        bufferParent.append(parent1[0][i])


    for i in range(punto,len(parent2[0]),1):
        #print i
        bufferParent.append(parent2[0][i])


    # Recombinación random ------ ------------------------ -----------

    # parentList = [ parent1, parent2 ]
    #
    #
    # bufferParent = []
    # for i in range(len(parent2[0])):
    #     #print i
    #     randomParent = random.randrange(0,2,1)
    #     randomParent = parentList[randomParent]
    #     bufferParent.append(randomParent[0][i])
    #


    # --------------------------------------------------------------


    # Creacion de nuevos objetos tipo periodo
    new_Parent = []
    for period in range(len(bufferParent)):
        section = bufferParent[period].section
        period = bufferParent[period].period
        day = bufferParent[period].day
        new_Period = createPeriod( section, period, day)
        new_Parent.append(new_Period)



    bufferReturn = [new_Parent ,parent1[1],parent2[2],parent2[3]]
    return bufferReturn
