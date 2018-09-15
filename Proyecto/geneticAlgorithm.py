#!/usr/bin/env python
# -*- coding: utf-8 -*-



class geneticAlgorithm(object):
    def __init__(self, g0, selection, fitness, crossover, mutation, goodValue):
        self.generations = [g0]
        self.selection = selection
        self.fitness = fitness
        self.crossover = crossover
        self.mutation = mutation
        self.goodValue = goodValue

    def execute_epoch(self):
        current_generation = self.generations[-1]
        pairs = self.selection(current_generation, self.fitness, self.goodValue)

        if(pairs == True):
            return pairs

        new_candidates = [
            self.crossover(pair[0], pair[1])
            for pair in pairs
        ]
        new_generation = [
            self.mutation(candidate)
            for candidate in new_candidates
        ]

        #sortData
        sortParent = []
        sortTeacher = []
        sortLab = []
        sortForbidden = []

        for parent in range(len(new_generation)):
            sortParent.append(new_generation[parent][0])
            sortTeacher.append(new_generation[parent][1])
            sortLab.append(new_generation[parent][2])
            sortForbidden.append(new_generation[parent][3])

        new_generation = []
        new_generation.append(sortParent)
        new_generation.append(sortTeacher)
        new_generation.append(sortLab)
        new_generation.append(sortForbidden)


        self.generations.append(new_generation)

        return False

    def optimize(self):
        while True: # TODO: criterio
            winnerParent = self.execute_epoch()
            if(winnerParent == True):
                break

        return self.generations[-1]
