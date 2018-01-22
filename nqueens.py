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

    def __init__(self, pop_size=100, cross_prob=0.11, mut_prob=0.045):
        self.___pop_size = pop_size
        self.__cross_prob = cross_prob
        self.__mut_prob = mut_prob


    '''
    Dummy method representing proper interface
    '''
    def get_first_generation(self):
        random.seed()
        temp_arr = []
        for i in range(0, self.___pop_size):
            temp_arr.append(bin(random.getrandbits(8 * 3))[2:].zfill(8 * 3))
        return temp_arr

    def get_phenotype(self, genotype=""): #WTF?
        phenotype = []
        for i in range(0, 24,3):
            bin_num=genotype[i:i + 3]
            num=int(bin_num,2)
            phenotype.append(num)
        return phenotype

    def get_fitness(self, phenotype=[]):
        fitness = 0   #Number of queens that beats each other. Assume that queens can beat throw others.
        a=phenotype
        for i in range(0, len(a)):
            for j in range (0, len(a)):
                if i!=j and( a[i] == a[j] or (a[i] - a[j] == i - j) or(a[i] - a[j] == j - i)):
                    fitness += 1
        return 1/(fitness/2+1)

    def crossover(self,parent1="",parent2=""):
        random.seed()
        point=random.randint(0,len(parent1))
        child1=parent1[0:point]+parent2[point:len(parent1)]
        child2=parent2[0:point]+parent1[point:len(parent1)]
        return child1,child2

    def get_new_generation(self,old_generation):
        random.seed();
        children=[]
        random.shuffle(old_generation)
        for i in range(0,len(old_generation)//2):
            child1,child2=self.crossover(old_generation[i],old_generation[i+1])
            children.append(child1)
            children.append(child2)
        children.extend(old_generation)
        children=self.select(children)
        return children

    def select(self,genotypes=[]): #halfs size of  population
        random.seed()
        temp = []
        result = []
        sum_fitness = 0

        for i in genotypes:
            fitness = self.get_fitness(self.get_phenotype(i))
            sum_fitness += fitness;
            temp.append([i, sum_fitness])
        random_nums = []

        for i in range(0, len(genotypes) // 2):
            random_nums.append(random.random() * sum_fitness)
        random_nums.sort()

        j=0
        for i in random_nums: #2 pointers method
            while i > temp[j][1]:
                j += 1
            result.append(temp[j][0])
        return result

    def get_mutated_generation(self,genotypes):
        random.seed()
        result=[]
        for i in genotypes:
            temp=i
            for j in range(0,len(temp)):
                if self.__mut_prob > random.random():
                    temp=temp[0:j] + str(int(temp[j], 2) ^ 1) + temp[j+1: len(temp)]
            result.append(temp)
        return result



    def get_best_fit_and_ph(self,genotypes=[]):
        max_fitness = 0
        best_ph = [];
        for i in genotypes:
            fitness = self.get_fitness(self.get_phenotype(i));
            if fitness > max_fitness:
                max_fitness = fitness
                best_ph=self.get_phenotype(i)
        return max_fitness, best_ph

    def get_visualization(self, phenotype):
        result=""
        for i in range(0,8):
            result=result+("+"*phenotype[i]+"Q"+"+"*(8-1-phenotype[i])+"\n")
        return result












    def solve(self, min_fitness=0.9, max_epochs=300):
        best_fit = None
        epoch_num = None
        visualization = None
        total_max_fit=0
        total_best_ph=[]
        curr_generation=self.get_first_generation()
        for i in range(0,max_epochs):
            max_fit,best_ph=self.get_best_fit_and_ph(curr_generation)
            if max_fit>total_max_fit:
                total_max_fit=max_fit
                total_best_ph=best_ph
            if total_max_fit>min_fitness:
                break
            curr_generation=self.get_new_generation(curr_generation)
            curr_generation=self.get_mutated_generation(curr_generation)
            print (len(curr_generation))
            epoch_num = i + 1;
        best_fit = total_max_fit
        visualization = self.get_visualization(total_best_ph)
        print(total_max_fit)
        print(total_best_ph)

        return best_fit, epoch_num, visualization
