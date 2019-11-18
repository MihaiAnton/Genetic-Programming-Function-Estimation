from Chromosome import Chromosome
from Population import Population
from Train import train
import numpy as np
from Functions import *
from Data import getData

from matplotlib import pyplot as plt

def f(x):
    # return x**2
    return np.sin(x)/(((x - np.pi/2)/np.pi))
    # return np.sin(x) * np.cos(x)

X = [[x] for x in np.arange(0,10,0.01)]
Y = [f(x[0]) for x in X]

# X,Y = getData("train")


p = Population(size=POPULATION,varCount=len(X[0]))



train(p, EPOCH_COUNT, X,Y)


best = p.getBest()

best.eval(X,Y)
print("MSE on test : " + str(best.phenotype))


Ypred = [best.computeFunction(x)[0] for x in X]

plt.plot([x[0] for x in X], Y, c = 'b',dashes=[6, 3])
plt.plot([x[0] for x in X], Ypred, c = 'r',dashes=[2,6])
plt.show()

