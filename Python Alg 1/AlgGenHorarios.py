# -*- coding: utf-8 -*-
"""
Created on Wed Jul 04 00:15:31 2018

@author: Ghost
"""

import random

def evaluacionDeLista(wantedList, actualList):
    scoreList = []
    score = 0
    rango = 0
    
    if(len(wantedList) >= len(actualList)):
        rango = len(actualList)
    else:
        rango = len(wantedList)
    
    print "rango"    
    print rango
    for i in range(rango):
        score = 1 - abs((wantedList[1] - actualList[1])/wantedList[1])
        print "score"    
        print score
        scoreList.append(score)
    return scoreList
        
    
def evaluacion(dia):
    M = [3,3]
    K = [3,2]
    P = [2]
    
    Mp = 1
    Kp = 1
    Pp = 1

    MpList = []
    KpList = []
    PpList = []
    
    for i in range(len(dia)-1):

        if dia[i] == dia[i+1]:

            if dia[i+1] == "0":
                Mp = Mp+1
            else:
                Mp = 1
                
            if dia[i+1] == "1":
                Kp = Kp+1
            else:
                Kp = 1
                
            if dia[i+1] == "2":
                Pp = Pp+1
            else:
                Pp = 1
                
#            print "######  "+str(i)+"  #####"
#            print Mp
#            print Kp
#            print Pp
            
        else:
            if Mp > 1:
                MpList.append(Mp)
            if Kp > 1:
                KpList.append(Kp)
            if Pp > 1:
                PpList.append(Pp)
                
            Mp = 1
            Kp = 1
            Pp = 1
            
#            print "######  "+str(i)+"  #####"
#            print Mp
#            print Kp
#            print Pp

    #Comienzo de evalucacion

    print MpList
    print KpList
    print PpList
    
    scoreMp =evaluacionDeLista(M,MpList)
    print "scoreList"    
    print scoreMp

lunes = ""
for i in range(18):
    lunes = lunes+str(random.randrange(0,3,1))


evaluacion(lunes)
print "\n############"
print lunes
for i in range(len(lunes)):
    print str(i)+" >>>> "+lunes[i]






