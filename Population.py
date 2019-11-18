import random

from Chromosome import Chromosome
from Functions import *
import numpy as np


class Population:

    def __init__(self, size=200, varCount=1):
        self.size = size
        self.varCount = varCount
        self.list = self.__createPopulation()

    def __createPopulation(self):
        """
            Creates a population of random chromosomes.
        :return: the population
        """
        pop = []
        for i in range(self.size):
            chrom = Chromosome()
            chrom.grow(TREE_DEPTH, self.varCount)
            pop.append(chrom)
        return pop

    def eval(self, input, output):
        """
            Evaluates all the chromosomes in the population, evaluating their fitness.
        :param input: the x values
        :param output: the y values which have to be predicted
        :return: None
        """
        i = 0
        for chrom in self.list:
            if i % FEEDBACK_EPOCH == 0:
                print("Evaluated chromosome {}.".format(i))
            i += 1
            chrom.eval(input, output)

    def getBest(self):
        """
            Returns the best chromosome.
        :return: the best chromosome.
        """
        bestPos = 0
        for i in range(1, len(self.list)):
            if self.list[i].phenotype < self.list[bestPos].phenotype:
                bestPos = i
        return self.list[bestPos]

    def replaceWorst(self, replacement):
        """
            Replaces the less fit chromosome in the population with a new one.
        :param replacement: the chromosome that will replace the worst current one
        :return: None
        """
        bestPos = 0
        for i in range(1, len(self.list)):
            if self.list[i].phenotype > self.list[bestPos].phenotype:
                bestPos = i
        self.list[bestPos] = replacement

    def selection(self):
        """
            Randomly selects a chromosome from the best half.
        :return: the selected chromosome.
        """
        self.list = sorted(self.list, key=lambda x:x.phenotype)
        limit = len(self.list)//2
        return self.list[random.randint(0,limit)]

    def XO(self, male : Chromosome, female : Chromosome):
        """
            Cross over operation between two chromosomes.
        :param male: male chromosome
        :param female: female chromosome
        :return: the 'child' chromosome
        """
        maleStart = random.randint(0,len(male.genotype)-1)
        femaleStart = random.randint(0,len(female.genotype)-1)

        _, maleEnd = male.computeFunction([1]*100, maleStart)
        _, femaleEnd = female.computeFunction([1]*100, femaleStart)
        chrom = Chromosome()
        chrom.variableCount, chrom.depth = male.variableCount, male.depth
        chrom.genotype = male.genotype[:maleStart] + female.genotype[femaleStart:femaleEnd] + male.genotype[maleEnd:]

        if chrom.getDepth()[0] > MAX_DEPTH:
            chrom.genotype = []
            chrom.grow(male.depth, male.variableCount)

        return chrom

    def mutation(self, chrom : Chromosome):
        """
            Performs a random mutation to the given chromosome.
        :param chrom: chromosome to mutate
        :return: the mutated chromosome
        """
        index = np.random.randint(0, len(chrom.genotype))

        elem = chrom.genotype[index]
        if isinstance(elem, float):
            chrom.genotype[index] = 1.0#random.random()
        elif elem in BINARY_FUNCTIONS:
            chrom.genotype[index] = random.choice(BINARY_FUNCTIONS)

        elif elem in UNARY_FUNCTIONS:
            chrom.genotype[index] = random.choice(UNARY_FUNCTIONS)
        return chrom



























