#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functions import showCompleteData as sortData
import collections

def generate_fitness(allLabs, allTeachers, forbiddenTime):

    def fitness(candidate):
        # TODO: return number, the higher the fitter

        #-------------- CRITERIOS DE PUNTOS ORIENTADO POSITIVO ---------------------
        # PUNTOS POSITIVOS
        closeTHPoints = 2500 #Puntos por periodos de Teoría cercanos
        closeLABPoints = 2500 #Puntos por periodos de lab cercanos
        sameDayPoints = 5000 #Puntos por periodos del mismo código en el mismo día
        periodForTeacherPoints = 200  #Puntos por ser un curso correcto para el profesor
        demandPositivePoints = 200  #Puntos por cumplir con las demandas
        repeatedPositivePoints = 1500  #Puntos por no repetir en teachers
        goodFTPoints = 500  #Puntos por no utilizar horarios prohibidos
        sameYearPositivePoints = 1500 #Puntos por no cruzar en el mismo año

        #Puntos NEGATIVOS
        overSizeLab = -2000 #Laboratorio con más periodos de su capacidad
        demandNegativePoints = -500  #Teacehr No cumple con su demanda
        repeatedNegativePoints = -3000  #En Teacher: horarios simultaneos
        badFTPoints = -2000   #Periodos Prohibidos
        sameYearNegativePoints = -2000 #Puntos por no cruzar en el mismo año



        scores = []
        completeData = []
        bufferScore = 0
        completeData = sortData(candidate)

        labCounter = {}
        demandCounter = {}
        usedForTeachers = {}
        yearCounter = {}

        for labCode in allLabs:
            labCounter.update( { labCode : 0 } )

        for teacher in allTeachers:
            demandCounter.update( { teacher : allTeachers[teacher].demandLeft })
            usedForTeachers.update( {teacher : []} )

        for i in range(1,6,1):
            yearCounter.update({ i : [[]] })

        #No Cruzar periodos del mismo año
        for period in candidate:
            bufferTime = [period.period , period.day]
            bufferPeriod = yearCounter[period.section.course.year]
            bufferPeriod.append(bufferTime)
            yearCounter[period.section.course.year] = bufferPeriod


        #Periodos Teoría cercanos
        for key in completeData:

            #Teacher Points iterations
            for teacher in allTeachers:
                #Demanda Cumplida
                if(key[2:] in demandCounter[teacher]):
                    if(teacher == completeData[key]['TH']['teacher']):
                        demandCounter[teacher][key[2:]]['TH'] = demandCounter[teacher][key[2:]]['TH'] - len(completeData[key]['TH']['periodos'])

                        for labCode in completeData[key]['LAB']:
                            if(completeData[key]['LAB'][labCode]['teacher'] == teacher):
                                demandCounter[teacher][key[2:]]['LAB'] = demandCounter[teacher][key[2:]]['LAB'] - len(completeData[key]['LAB'][labCode]['periodos'])

                #Periodos utilizados en teacher
                if(completeData[key]['TH']['teacher'] == teacher):
                    for periods in completeData[key]['TH']['periodos']:
                        usedForTeachers[teacher].append(periods)

                for labCode in completeData[key]['LAB']:
                    if(completeData[key]['LAB'][labCode]['teacher'] == teacher):
                        for periods in completeData[key]['LAB'][labCode]['periodos']:
                            usedForTeachers[teacher].append(periods)

            #Periodos TH
            periodos = completeData[key]['TH']['periodos']

            for p in range(len(periodos) - 1):
                if(periodos[p][1] == periodos[p+1][1]):
                    bufferScore = bufferScore + sameDayPoints  #Mismo día
                if( abs(periodos[p][0] - periodos[p+1][0]) == 1):
                    bufferScore = bufferScore + closeTHPoints #Un periodo cerca
                if( abs(periodos[p][0] - periodos[p+1][0]) == 2):
                    bufferScore = bufferScore +  closeTHPoints #A dos periodos cerca
                #Forbidden teorías


            # Puntos por horario correcto para su profesor
            for p in range(len(periodos)):
                if(periodos[p] in allTeachers[completeData[key]['TH']['teacher']].prettyWorkTime):
                    bufferScore = bufferScore + periodForTeacherPoints #Periodo correcto para el profesor

            #Periodos LAB
            for labCode in completeData[key]['LAB']:
                periodos = completeData[key]['LAB'][labCode]['periodos']
                for p in range(len(periodos) - 1):
                    if(periodos[p][1] == periodos[p+1][1]):  #Mismo día
                        bufferScore = bufferScore + sameDayPoints
                    if( abs(periodos[p][0] - periodos[p+1][0]) == 1):
                        bufferScore = bufferScore + closeLABPoints #Un periodo cerca
                    if( abs(periodos[p][0] - periodos[p+1][0]) == 2):
                        bufferScore = bufferScore + closeLABPoints #Segundo periodo cerca
                labCounter[completeData[key]['LAB'][labCode]['numLab']] = labCounter[completeData[key]['LAB'][labCode]['numLab']] + 1 #Sumando Cantidad de Laboratorios actuales


            # Puntos por horario correcto para su profesor
                for p in range(len(periodos)):
                    if(periodos[p] in allTeachers[completeData[key]['LAB'][labCode]['teacher']].prettyWorkTime):
                        bufferScore = bufferScore + periodForTeacherPoints #Periodo correcto para el profesor


        #Puntos por laboratorio Excedido
        for labNumber in labCounter:
            if(labCounter[labNumber] > 85):
                bufferScore = bufferScore + overSizeLab


        #Puntos por demanda Cumplida
        for teacher in demandCounter:
            for code in demandCounter[teacher]:
                if(demandCounter[teacher][code]['TH'] == 0):
                    bufferScore = bufferScore + demandPositivePoints
                else:
                    bufferScore = bufferScore + demandNegativePoints
                if(demandCounter[teacher][code]['LAB']== 0):
                    bufferScore = bufferScore + demandPositivePoints
                else:
                    bufferScore = bufferScore + demandNegativePoints

        #Puntos por no tener periodos repetidos
        for teacher in usedForTeachers:
            originalLen = len(usedForTeachers[teacher])
            bufferList = set(map(tuple,usedForTeachers[teacher]))
            bufferList = map(list,bufferList)
            repetidos = originalLen - len(bufferList)
            if(repetidos == 0):
                bufferScore = bufferScore + repeatedPositivePoints
            else:
                bufferScore = bufferScore + repetidos*repeatedNegativePoints

        #forbiddenTime iterations
        for time in forbiddenTime:
            for period in range(len(candidate)):
                p = [ candidate[period].period , candidate[period].day ]

                if(p in time.prettyForbiddenTime):
                    if(int(time.year[-1:]) == candidate[period].section.course.year):
                        bufferScore = bufferScore + badFTPoints
                    else:
                        bufferScore = bufferScore + goodFTPoints

        #Same year iteracions

        for year in yearCounter:
            originalLen = len(yearCounter[year])
            bufferList = set(map(tuple,yearCounter[year]))
            bufferList = map(list,bufferList)
            repetidos = originalLen - len(bufferList)
            if(repetidos == 0):
                bufferScore = bufferScore + sameYearPositivePoints
            else:
                bufferScore = bufferScore + repetidos*sameYearNegativePoints
                
        return bufferScore

    return fitness
