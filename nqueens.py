# -*- coding: utf-8 -*-
import random
import math


class Solver_8_queens:

    def __init__(self, pop_size=200, cross_prob=0.1, mut_prob=0.045):
        self.___pop_size = pop_size
        self.__cross_prob = cross_prob
        self.__mut_prob = mut_prob
        self.__curr_generation = []
        self.__board_size = 8
        self.__gen_size = int(math.ceil(math.log(self.__board_size, 2)))
        self.best_fitness = 0
        self.best_genotype = 0
        pass

    def get_random_generation(self):
        random.seed()
        temp_arr = []
        for i in range(0, self.___pop_size):
            temp_arr.append(random.getrandbits(self.__board_size * self.__gen_size))
        return temp_arr

    def get_phenotype(self, genotype=0):
        phenotype = []
        pos = (1 << self.__gen_size) - 1 #pos=111 bin
        temp_gen = genotype
        for i in range(0, self.__board_size):
            phenotype.append(temp_gen & pos)
            temp_gen = temp_gen >> self.__gen_size
        return phenotype

    def get_fitness(self, phenotype):
        fitness = 0  # Number of queens that beats each other. Assume that queens can beat throw others.
        a = phenotype
        for i in range(0, len(a)):
            for j in range(0, i):
                if (a[i] == a[j] or (math.fabs(a[i] - a[j]) == (i - j))):
                    fitness += 1
        return 1 / (fitness + 1)

    def crossover(self, parent1=0, parent2=0):
        random.seed()
        if self.__cross_prob > random.random():
            point = random.randint(0, self.__board_size * self.__gen_size)
            div_line = 1 << point
            child1 = parent1 // div_line * div_line + parent2 % div_line
            child2 = parent2 // div_line * div_line + parent1 % div_line
            return child1, child2
        else:
            return parent1, parent2

    def get_next_generation(self, old_generation):
        random.seed()
        children = []
        random.shuffle(old_generation)
        for i in range(0, len(old_generation), 2):
            child1, child2 = self.crossover(old_generation[i], old_generation[i+1])
            children.append(child1)
            children.append(child2)
        children.extend(old_generation)
        return children

    def select(self, genotypes): #result has popsize genotypes
        #Careful. Call changes class variables: best_fitness, best_genotype
        # explanation of realization
        #We have array of pairs genotype-sum_fitness,  fitness for another purpose
        #genotype with index i has "bucket" from sum_fitness[i]-fitness(genotype) to sum_fitness
        #If random number in range(0,total_sum_fitness) gets in "bucket" we take genotype in result
        #So probubility of getting genotype in next generation is proportional to its fitness
        random.seed()
        temp = []
        result = []
        sum_fitness = 0

        for i in genotypes:
            fitness = self.get_fitness(self.get_phenotype(i))
            sum_fitness += fitness;
            temp.append([i, sum_fitness, fitness])
        random_nums = []

        for i in range(0, self.___pop_size):
            random_nums.append(random.random() * sum_fitness)
        random_nums.sort()

        j = 0
        for i in random_nums:  # 2 pointers method
            while i > temp[j][1]:
                j += 1
            result.append(temp[j][0])
            if temp[j][2] > self.best_fitness:
                self.best_fitness = temp[j][2]
                self.best_genotype = temp[j][0]
        return result

    def get_mutated_generation(self, genotypes):
        random.seed()
        result = []
        for i in genotypes:
            temp = i
            for j in range(0, self.__board_size*self.__gen_size):
                if self.__mut_prob > random.random():
                    temp = temp ^ 1 << j
            result.append(temp)
        return result

    def get_visualization(self, phenotype):
        result = ""
        for i in range(0, 8):
            result = result + ("+" * phenotype[i] + "Q" + "+" * (self.__board_size - 1 - phenotype[i]) + "\n")
        return result

    def solve(self, min_fitness=0.9, max_epochs=200):
        if (min_fitness is None) or (max_epochs is None):
            return 0, 0, None
        curr_epoch = 0
        curr_generation = self.get_random_generation()
        while (min_fitness > self.best_fitness) and (curr_epoch < max_epochs):
            curr_epoch += 1
            curr_generation = self.get_next_generation(curr_generation)
            curr_generation = self.get_mutated_generation(curr_generation)
            curr_generation = self.select(curr_generation)  # updates self.best_genotype , self.best_fitness
        visualization = self.get_visualization(self.get_phenotype(self.best_genotype))
        return self.best_fitness, curr_epoch, visualization
