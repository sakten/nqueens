# -*- coding: utf-8 -*-
import  random
class Solver_8_queens:
    '''
    Dummy constructor representing proper interface
    '''
    ___pop_size = 0
    __cross_prob = 0
    __mut_prob = 0
    __curr_generation = []

    def __init__(self, pop_size=1000, cross_prob=0.11, mut_prob=0.05):
        self.___pop_size = pop_size
        self.__cross_prob - cross_prob
        self.__mut_prob = mut_prob


    '''
    Dummy method representing proper interface
    '''
    def generate_random(self, pop_size):
        random.seed()
        temp_arr = []
        for i in range(0, pop_size):
            temp_arr.append(bin(random.getrandbits(8 * 3))[2:].zfill(8 * 3))
        self.__curr_generation = temp_arr

    def get_phenotype(self, genotype):
        phenotype = []
        for i in range(0, 8):
            phenotype.append(genotype[i:i + 3])
        return phenotype

    def get_fitness(self, phenotype=[]):
        fitness = 0
        a=phenotype
        for i in range(0, len(a)):
            for j in range (0, len(a)):
                if i!=j and( a[i] == a[j] or (a[i] - a[j] == i - j) or(a[i] - a[j] == j - i)):
                    fitness += 1
        return fitness/2  #Number of queens that beats each other. Assume that queens can beat throw others.

    def crossover(self,parent1="",parent2=""):
        random.seed()
        point=random.randint(len(parent1))
        child1=parent1[0:point]+parent2[point:len(parent1)]
        child2=parent2[0:point]+parent1[point:len(parent1)]
        return child1,child2

    def solve(self, min_fitness=0.9, max_epochs=100):
        best_fit = None
        epoch_num = None
        visualization = None
        return best_fit, epoch_num, visualization
