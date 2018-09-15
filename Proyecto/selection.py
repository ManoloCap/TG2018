#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import random


def selection(generation, fitness, goodValue):
    # TODO: return list of 2D tuples (candidate, candidate)
    #Puntos para hacer beak
    scores = fitness(generation)



    [parents, allLabs, allTeachers, forbiddenTime] = generation
    [parentsC, allLabsC, allTeachersC, forbiddenTimeC] = generation


    #CRITERIO Selección de los mejores
    betterPairs = int(len(parents)*0.65)


    betterParentsList = []
    betterLabList = []
    betterTeacherList = []
    betterForbiddenList = []

    #DETENER ALG SI SE CONSIGUE UNA MUY BUENA GENERACON -----------------------
    for points in scores:
        if(points > goodValue):
            return True
    # ------------------------
    for pair in range(betterPairs):
        betterI = np.argmax(scores)

        betterParentsList.append(parentsC[betterI])
        betterLabList.append(allLabsC[betterI])
        betterTeacherList .append(allTeachersC[betterI])
        betterForbiddenList .append(forbiddenTimeC[betterI])
        scores[betterI] = -999999


    #print len(betterParentsList)

    pairs = []
    counter = 0
    bufferValue = 0
    while counter != len(parents):
        i = random.randrange(0,len(parents),1)
        pairBuffer = [parents[i], allLabs[i], allTeachers[i], forbiddenTime[i]]
        #print bufferValue
        pairBuffer2 = [ betterParentsList[bufferValue] , betterLabList[bufferValue], betterTeacherList[bufferValue], betterForbiddenList[bufferValue]]
        pairs.append([pairBuffer, pairBuffer2])

        if(counter >= len(betterParentsList) -1 ):
            bufferValue = 0
        else:
            bufferValue = bufferValue + 1

        counter = counter  + 1

    # print len(pairs[0])
    # print "JEJE"


    return pairs
