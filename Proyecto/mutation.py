#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from objects import period as createPeriod
def generate_mutation(allLabs, allTeachers, forbiddenTime):


    def mutatePeriod(period):

        actual_Code = period.code
        actual_Section = period.section

        mutated_Day = random.randrange(0, 17 , 1)
        mutated_Period = random.randrange(0, 5, 1)
        mutated_Teacher = random.choice(allTeachers.keys())
        if(actual_Section.labNumber != ''):
            mutated_Lab = random.choice(allLabs.keys())
        else:
            mutated_Lab = ''

        new_Period = createPeriod( actual_Section,
                    mutated_Day,
                    mutated_Period,
                    mutated_Teacher,
                    actual_Code)

        return new_Period

    def mutation(candidate):
    # TODO: return new candidate
        #cantidad de mutaciones máximas
        probability = 0.02 # Probabilidad de mutar de 0 a 1

        #Mutaciones reales

        #--------------------------
        probability = 1 - probability
        for periodPosition in range(len(candidate)):
            do_Mutation = random.randrange(0, 100, 1)
            if(do_Mutation >= probability*100):
                candidate[periodPosition] = mutatePeriod(candidate[periodPosition])
                #print "YES"
                #print do_Mutation


        return candidate

    return mutation
