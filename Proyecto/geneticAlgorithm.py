#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pydash as py_
import gc




class geneticAlgorithm(object):
    def __init__(self, g0, selection, fitness, crossover, mutation, max_generations, logger, exitDataToExcel, saveData,printProcess):
        self.generations = [g0]
        self.selection = selection
        self.fitness = fitness
        self.crossover = crossover
        self.mutation = mutation
        self.scores = []
        self.max_generations = max_generations
        self.logger = logger
        self.bestIndividual = ''
        self.generationCounter = 0
        self.saveData = saveData
        self.printProcess = printProcess
        self.exitDataToExcel = exitDataToExcel
        self.scoreData = []

    def execute_epoch(self):
        #print len(self.generations[-1])
        current_generation = self.generations[-1]
        pairs, sorted_scores = self.selection(current_generation, self.fitness)

        new_candidates = [
            self.crossover(pair[0], pair[1])
            for pair in pairs
        ]
        flat_candidates = py_.flatten(new_candidates)

        new_generation = [
            self.mutation(candidate)
            for candidate in flat_candidates
        ]

        self.generations.append(new_generation)
        if(len(self.generations) > 50):
            self.generations.pop(0)




        #DataExtract
        self.bestIndividual = self.logger(sorted_scores[0], self.bestIndividual, False)
        self.generationCounter = self.generationCounter + 1

        self.scoreData.append(self.bestIndividual['score'])
        self.saveData(self.scoreData)
        self.printProcess(str(sorted_scores[0]['score']), str(self.bestIndividual['score']), self.generationCounter)

        #Excel maxGenerations
        self.exitDataToExcel(self.bestIndividual['individual'], self.generationCounter)

        #END DataExtract
    def optimize(self):
        for iteration in range(self.max_generations):
            self.execute_epoch()
            gc.collect()
            #print self.bestIndividual
        return self.bestIndividual
