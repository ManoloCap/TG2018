#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
import numpy as np
import random

OUTSTANDING_PERCENTAGE = 0.65
MAX_PAIRS = 2000
def selection(generation, fitness):
    # Selection : return list of 2D tuples (candidate, candidate)

    scores = []
    for individual in generation:

        scores.append({
            'individual': individual,
            'score': int(fitness(individual))
        })

    sorted_scores = sorted(scores, key=lambda item: item['score'], reverse=True)


    if(int(len(sorted_scores) * OUTSTANDING_PERCENTAGE) % 2 == 0):
        elite_length = int(len(sorted_scores) * OUTSTANDING_PERCENTAGE)
    else:
        elite_length = int(len(sorted_scores) * OUTSTANDING_PERCENTAGE) + 1

    elite = sorted_scores[0:elite_length]
    pairs = []

    for pairNumber in range(len(elite)-1):
        #print 'p1 :' + str(elite[pairNumber]['score'])+" - p2 : "+str(elite[pairNumber+1]['score'])
        pairs.append([elite[pairNumber]['individual'], elite[pairNumber+1]['individual']])
        if(len(pairs) >= MAX_PAIRS/3):
            break

    return (pairs, sorted_scores)
