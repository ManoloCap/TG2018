#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 23:26:28 2018

@author: Ghost
"""
import random
import functions
import objects
import jsonpickle

def generate():
    #------------- VARIABLES EDITABLES DEL ALGORITMO  ------------------------
    labs= 2
    finalSolution = []
    poblation = 3         #INGRESAR CANTIDAD DE INDIVIDUOS
    generations  = 500    #INGRESAR CANTIDAD MÁXIMA DE GENERACONES
    generation = []
    miniumValueToBreak = 1000   # Puntaje minimo para desplegar Solucion
    winnerPosition = 0
    miniumValue = False
    mutations = 200
    maxNumber = 1
    minNumber = 1
    showScores = True
    #-----------------------Labs for all the poblation -------------------------------
    allLabs = []
    bufferIndividual = {}
    for individual in range(poblation):
        for i in range(labs):
            bufferLab = objects.laboratory(i)
            bufferIndividual.update( { bufferLab.number  : bufferLab})
        allLabs.append(bufferIndividual)
        bufferIndividual = {}

    #print allLabs[0][0].time

    #print allLabs
    #------------- Importando y limpiando demanda  ------------------------
    demand = functions.getDemandList('data/demanda2018Ciclo2.xlsx', 'Hoja2')
    #print functions.letJustDepartmentDemand(demand)
    #print demand
    #-------------Agregar para n planes----------
    dataPlanM2016 = functions.getDataList('data/planM2016.csv')
    dataPlanE2016 = functions.getDataList('data/planE2016.csv')
    #Talvez agregar Plan Viejo M
    #Talvez agregar plan Viejo E


     #------------- Creando Objetos de los cursos para el semestre en funcion de la demanda ----------
    maxTheory = 30  # Numero maximo de estudiantes por seccion
    maxLeftOver = 3 # Numero maximo de estudiantes que pueden quedar de mas aparte de los 15 por seccion antes de abrir una nueva

    allCourses = functions.mergeAllCourses([dataPlanE2016, dataPlanM2016,],
                                            functions.letJustDepartmentDemand(demand),
                                            maxTheory,
                                            maxLeftOver)


    #print allCourses
    #for i in range(len(allCourses)): print allCourses[i].code #Ver cursos a programar

    allTeachers = []
    #------------- Importando profesores ------------------------
    for i in range(poblation):
        allTeachers.append(functions.readTeachers('data/profesores.xlsx', allCourses))

    #print allTeachers[0][allTeachers[0].keys()[0]].name
    #print allTeachers[0][allTeachers[0].keys()[0]].prettyWorkTime

    # ----------------- Adding forbiddenTime ---------------------------
    forbiddenTime = []
    for i in range(poblation):
        forbiddenTime.append(functions.loadForbiddens('data/horariosProhibidos.xlsx'))

    #print ""
    #print forbiddenTime[0][0].prettyForbiddenTime

    #for i in range(len(forbiddenTime)):
    #    pprint(forbiddenTime[i])

    #--------------------------- Verify Av. -------------------------
    verifyData = []
    for i in range(poblation):
        verifyData.append(functions.verifyTeacherAv(allTeachers[i], allCourses))

    #print verifyData


    # --------------  PARTE ASIGNACIÓN DE HORARIOS -------------------

    labMax = 15
    labLeftOver =  4

    allSections = functions.InitialSolution(allCourses, labMax, labLeftOver, labs)


    # Contador secciones para cada curso dentro del vector solución
    contadorSeccionesTH = {}
    contadorSeccionesLAB = {}

    for i in range(len(allSections)):
        if(allSections[i].course.code in contadorSeccionesLAB or allSections[i].course.code in contadorSeccionesTH ):

            if(allSections[i].classType == 'TH'):
                contadorSeccionesTH.update( { allSections[i].course.code : contadorSeccionesTH[allSections[i].course.code] + 1 } )
            elif(allSections[i].classType == 'LAB'):
                contadorSeccionesLAB.update( { allSections[i].course.code : contadorSeccionesLAB[allSections[i].course.code] + 1 } )

        else:
            if(allSections[i].classType == 'TH'):
                contadorSeccionesTH.update( { allSections[i].course.code : 1 } )

                if(int(allSections[i].course.labPeriods) != 0):
                    contadorSeccionesLAB.update( { allSections[i].course.code : 0 } )

            elif(allSections[i].classType == 'LAB'):
                contadorSeccionesLAB.update( { allSections[i].course.code : 1 } )

                if(int(allSections[i].course.theoryPeriods) != 0):
                    contadorSeccionesTH.update( { allSections[i].course.code : 0 } )


    #   mostrar contadores
    print contadorSeccionesTH
    print contadorSeccionesLAB

    #print len(allSections)
    #for i in range(len(allSections)):
    #    print allSections[i].code


    # -----------------AHORA A PARTIR DE LAS SECCIONES SE VAN A GENERAR "PERIODOS" -----------------
    allPeriods = [] #Esta contendra toda la información para realizar un fitness
    allPeriodsBuffer = []
    for pob in range(poblation):
        for i in range(len(allSections)):

            classType = allSections[i].classType
            periods = 0
            if(classType == 'LAB'):
                periods = int(allSections[i].course.labPeriods)
                labCount = 0
                thVar = 0
                for p in range(periods):

                    assignPeriod = { allSections[i].code : allSections[i] }
                    allPeriodsBuffer.append(assignPeriod)

                    if(labCount == 2):
                        labCount = 0

                    #print assignPeriod

            elif(classType == 'TH'):
                periods = int(allSections[i].course.theoryPeriods)

                for p in range(periods):
                    assignPeriod = { allSections[i].code : allSections[i] }
                    allPeriodsBuffer.append(assignPeriod)
                    #print assignPeriods

        allPeriods.append(allPeriodsBuffer)
        allPeriodsBuffer = []

    #print "PERIODOS: "
    #print len(allPeriods[5])
    periodCounter = {}
    teoriaCounter = 0
    labCounter = 0
    teacherPeriod = {}

    return allPeriods
