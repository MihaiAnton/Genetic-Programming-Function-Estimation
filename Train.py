
from Population import *

def train(population : Population, epochCount, input, output):
    """
        For a certain number of epochs, perform the following:
            1. Get the current best chromosome.
            2. Select 2 random parent chromosomes.
            3. Create an offspring(child) of those two selected.
            4. Perform a random mutation on the child.
            5. Replace the least fit member of the population with the child resulted above.
    :param population: The initial population
    :param epochCount: How many epochs to run the algorithms
    :param input: the x variables
    :param output: the y variables to predict, based on the input
    :return: None
    """
    population.eval(input, output)

    for epoch in range(epochCount):
        if epoch % FEEDBACK_EPOCH == 0:
            best = population.getBest()
            print("Epoch " + str(epoch) + " genotype: " + str(best.genotype) + " loss: " + str(best.phenotype))
            if best.phenotype == 0:
                break

        male = population.selection()
        female = population.selection()
        off = population.XO(male, female)
        offM = population.mutation(off)

        offM.eval(input, output)
        population.replaceWorst(offM)
