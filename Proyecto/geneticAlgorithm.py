#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pydash as py_
class geneticAlgorithm(object):
    def __init__(self, g0, selection, fitness, crossover, mutation, max_generations, logger):
        self.generations = [g0]
        self.selection = selection
        self.fitness = fitness
        self.crossover = crossover
        self.mutation = mutation
        self.scores = []
        self.max_generations = max_generations
        self.logger = logger
        self.bestIndividual = ''

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

        #Temporal para prints
        self.bestIndividual = self.logger(sorted_scores[0], self.bestIndividual)
        print 'Actual Generation Best Score: '+str(sorted_scores[0]['score'])
        print 'Best of Bests: '+str(self.bestIndividual['score'])

    def optimize(self):
        for iteration in range(self.max_generations):
            self.execute_epoch()
            #print self.bestIndividual
        return self.generations[-1][0]
