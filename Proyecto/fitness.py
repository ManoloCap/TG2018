#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functions import showCompleteData as sortData
import collections
import copy
from collections import Counter
def generate_fitness(allLabs, allTeachers, forbiddenTime):

    def fitness(candidate):
        #print len(candidate)
        # Sort Data  ---------------------------------------------------
        completeData = sortData(candidate)
        # valueTeacherBuffers -------------------------------------------
        teacherDemand = {} #Buffer Demanda del profesor
        teachersUsedTime = {} #Buffer periodos ocupados para cada profesor
        for teacher in allTeachers:
            teacherDemand.update({ teacher : copy.deepcopy(allTeachers[teacher].demandLeft) })
            teachersUsedTime.update({teacher: []})
        # yearBuffer ---------------
        yearBuffer = {}
        for period in candidate:
            period_Year = period.section.course.year
            position = [period.period,period.day]

            if(period_Year in yearBuffer):
                period_Year_Buffer = yearBuffer[period_Year]
                period_Year_Buffer.append(position)
                yearBuffer.update( {period_Year : period_Year_Buffer})

            else:
                yearBuffer.update({period_Year : [position]})


        #---------------------- POINTS ----------------------------
        score = 0
        #---------------------- Teachers ----------------------------
        course_that_teacher_want = 10 #Periodo perteneciente a un curso que el profesor quiere.
        teacher_Time_Right = 1 #Periodo no interfiere con el horario seleccionado por el profesor.
        teacher_No_Repeat_Period = 2 # El profesor no debe tener dos periodos al mismo día y periodo.

        #---------------------- Theory and Lab Period points ----------------------------
        close_Period = 10 #Periodos cercanos
        repeated_Period = 1 #Evitar periodos repetidos
        sameDay_Period = 1 #Periodos impartidos el mismo día

        # ------------------------ Forbidden Time Points -------------------------
        forbidden_Time_Points = 1 #Puntos para evitar los horarios prohibidos en el año específico

        # ---------- Year Points ------------------
        no_Repeat_Same_Course = 1 #Se permiten secciones en la misma hora, con diferente profesor
        good_Time_Year = 10 # Primero y segundo año en la mañana, tercero, cuarto y quinto en la tarde (TH)
        #Teachers points
        for period in candidate:
            position = [period.period,period.day]
            course_Code = period.section.course.code
            section_Code = period.code
            course_Teacher = period.teacher
            class_Type = period.section.classType


            # --------------------------------------- TEACHERS POINTS  --------------------------------------------
            if(course_Code in teacherDemand[course_Teacher]):

                #---------------------  Course_that_teacher_want  POINTS ------------------------  MAX POINTS: len(candidate)*nPoints
                #PUEDE MEJORAR!

                if(teacherDemand[course_Teacher][course_Code][class_Type] > 0):
                    score = score + course_that_teacher_want
                    teacherDemand[course_Teacher][course_Code][class_Type] = teacherDemand[course_Teacher][course_Code][class_Type] -1
                else:
                    score = score - score + course_that_teacher_want

                #---------------------  Course_that_teacher_want  END ------------------------


                #---------------------  teacher_Time_Right  POINTS ------------------------ MAX POINTS: len(candidate)*nPoints
                # PUEDE MEJORAR!
                if(position in allTeachers[course_Teacher].prettyWorkTime):
                    score = score + teacher_Time_Right
                else:
                    score = score - teacher_Time_Right

                #---------------------  teacher_Time_Right   END ------------------------

                #--------------------- teacher_No_Repeat_Period  POINTS ------------------------  MAX POINTS: len(candidate)*nPoints
                if(position not in teachersUsedTime[teacher]):
                    score = score + teacher_No_Repeat_Period
                    teachersUsedTime[teacher].append(position)
                else:
                    score = score - teacher_No_Repeat_Period
                #---------------------  teacher_No_Repeat_Period   END ------------------------

            # --------------------------------------- TEACHERS END --------------------------------------------
            # --------------------------------------- THEORY POINTS --------------------------------------------

        #Theory and LAB periods position
        for section_Code in completeData:
            # ----------------------- Theory POINTS --------------------------
            bufferPeriods = completeData[section_Code]['TH']['periodos']

            # ------------  Close Period Cases POINS   ------------------  MAX POINTS: len(candidate con N peiodos)*nPoints*N
            # 2 period case --------
            if(len(bufferPeriods) == 2):
                period_TimeA = bufferPeriods[0]
                period_TimeB = bufferPeriods[1]
                # CLOSE PERIOD
                if(abs(period_TimeA[0] - period_TimeB[0]) == 1):
                    score = score + close_Period
                else:
                    sore = score - close_Period
                # SAME DAY
                if(period_TimeA[1] == period_TimeB[1]):
                    score = score + sameDay_Period
                else:
                    score = score - sameDay_Period
                # repeated
                if(period_TimeA != period_TimeB):
                    score = score + repeated_Period
                else:
                    score = score - repeated_Period

            # 3 period case --------
            if(len(bufferPeriods) == 3):
                period_TimeA = bufferPeriods[0]
                period_TimeB = bufferPeriods[1]
                period_TimeC = bufferPeriods[2]

                # Close to A
                if(period_TimeA[0] - period_TimeB[0] == -1 and
                   period_TimeA[0] - period_TimeC[0] == 1):
                    score = score + close_Period
                # Close to B
                elif(period_TimeB[0] - period_TimeA[0] == -1 and
                     period_TimeB[0] - period_TimeC[0] == 1):
                    score = score + close_Period
                # Close to C
                elif(period_TimeC[0] - period_TimeB[0] == -1 and
                     period_TimeC[0] - period_TimeC[0] == 1):
                    score = score + close_Period

                # No Close
                else:
                    sore = score - close_Period

                # A and B Same Day
                if(period_TimeA[1] == period_TimeB[1]):
                    score = score + sameDay_Period
                # A and C Same Day
                if(period_TimeA[1] == period_TimeC[1]):
                    score = score + sameDay_Period
                # B and C Same Day
                if(period_TimeB[1] == period_TimeC[1]):
                    score = score + sameDay_Period
                # No Same Day
                else:
                    score = score - sameDay_Period

                # repeated
                if(period_TimeA != period_TimeB):
                    score = score + repeated_Period
                elif(period_TimeA != period_TimeC):
                    score = score + repeated_Period
                elif(period_TimeB != period_TimeC):
                    score = score + repeated_Period
                else:
                    score = score - repeated_Period
                #PUEDE SER: PUNTOS POR LA MISMA HORA CON DIFERENTE DIA EN CASO DE NO TENER EL MISMO DIA.

            # ------------  Close Period Cases END   ------------------

        # ----------------------- Theory END --------------------------

        # ----------------------- LAB POINTS --------------------------

            for section_LAB in completeData[section_Code]['LAB']:
                bufferPeriods = completeData[section_Code]['LAB'][section_LAB]['periodos']

                # ------------  Close Period Cases POINS   ------------------  MAX POINTS: len(candidate con N peiodos)*nPoints*N
                # 2 period case --------
                if(len(bufferPeriods) == 2):
                    period_TimeA = bufferPeriods[0]
                    period_TimeB = bufferPeriods[1]
                    # CLOSE PERIOD
                    if(abs(period_TimeA[0] - period_TimeB[0]) == 1):
                        score = score + close_Period
                    else:
                        sore = score - close_Period
                    # SAME DAY
                    if(period_TimeA[1] == period_TimeB[1]):
                        score = score + sameDay_Period
                    else:
                        score = score - sameDay_Period
                    # repeated
                    if(period_TimeA != period_TimeB):
                        score = score + repeated_Period
                    else:
                        score = score - repeated_Period
                # 3 period case --------
                if(len(bufferPeriods) == 3):
                    period_TimeA = bufferPeriods[0]
                    period_TimeB = bufferPeriods[1]
                    period_TimeC = bufferPeriods[2]

                    # Close to A
                    if(period_TimeA[0] - period_TimeB[0] == -1 and
                       period_TimeA[0] - period_TimeC[0] == 1):
                        score = score + close_Period
                    # Close to B
                    elif(period_TimeB[0] - period_TimeA[0] == -1 and
                         period_TimeB[0] - period_TimeC[0] == 1):
                        score = score + close_Period
                    # Close to C
                    elif(period_TimeC[0] - period_TimeB[0] == -1 and
                         period_TimeC[0] - period_TimeC[0] == 1):
                        score = score + close_Period

                    # No Close
                    else:
                        sore = score - close_Period

                    # A and B Same Day
                    if(period_TimeA[1] == period_TimeB[1]):
                        score = score + sameDay_Period
                    # A and C Same Day
                    if(period_TimeA[1] == period_TimeC[1]):
                        score = score + sameDay_Period
                    # B and C Same Day
                    if(period_TimeB[1] == period_TimeC[1]):
                        score = score + sameDay_Period
                    # No Same Day
                    else:
                        score = score - sameDay_Period

                # repeated
                if(period_TimeA != period_TimeB):
                    score = score + repeated_Period
                elif(period_TimeA != period_TimeC):
                    score = score + repeated_Period
                elif(period_TimeB != period_TimeC):
                    score = score + repeated_Period
                else:
                    score = score - repeated_Period
                    #PUEDE SER: PUNTOS POR LA MISMA HORA CON DIFERENTE DIA EN CASO DE NO TENER EL MISMO DIA.

                # ------------  Close Period Cases END   ------------------

        # ----------------------- LAB END --------------------------

        #Year points:
        # ---------------------- YEAR POINTS -------------------------
        repeated = 0
        for year in yearBuffer:
            #print yearBuffer[year]
            bufferSET = Counter([tuple(t) for t in yearBuffer[year]])
            #print bufferSET
            for element in bufferSET:
                repeated = repeated + bufferSET[element] - 1


        # ------------------ No repeated Year POINTS ------------------ MAX POINTS = 0
        score = score - no_Repeat_Same_Course*repeated
        # ------------------ No repeated Year END ------------------ MAX POINTS: len(candidate)*nPoints

        for period in candidate:
            period_Year = period.section.course.year
            position = period.period
            if(period_Year == 1):
                if(position <= 8):
                    score = score + good_Time_Year
                else:
                    score = score - good_Time_Year
            elif(period_Year == 2):
                if(position <= 11):
                    score = score + good_Time_Year
                else:
                    score = score - good_Time_Year
            else:
                if(position >= 8):
                    score = score + good_Time_Year
                else:
                    score = score - good_Time_Year
         # ---------------------- YEAR END -------------------------

        # Forbidden time
        # --------------- forbidden_Time_Points POINTS -------------------
        for period in candidate:
            period_Period = period.period
            period_Day = period.day
            period_Year = period.section.course.year
            for position in forbiddenTime[period_Year-1].prettyForbiddenTime:
                if(period_Period != position[0] and
                   period_Day != position[1]):
                   score = score + forbidden_Time_Points
                else:
                    score = score - forbidden_Time_Points
        # --------------- forbidden_Time_Points END -------------------
        return score

    return fitness
