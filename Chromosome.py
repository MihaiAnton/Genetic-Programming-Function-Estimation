
from Functions import *
import random
import warnings
from numpy import sin,cos,tanh,arccos,arcsin,exp,log,tan as tangent

# warnings.filterwarnings("error")

class Chromosome:
    """
        Class that holds all the information from a chromosome.
    """
    def __init__(self):
        """
            Chromosome initializer
            self.genotype holds a preorder traversal of the function tree
        """
        self.genotype = []
        self.phenotype = 0
        self.depth = None
        self.variableCount = None


    def scale(self,x,low,high):
        """
            Limits value x between [low, high]
        :param x:
        :param low:
        :param high:
        :return: the limited value
        """
        x = min(x,high)
        x = max(x,low)
        return x


    def grow(self, depth, variableCount):
        """
            Grows the function tree.
        :param depth: maximum depth allowed
        :param variableCount: how many variables are in the input data
        :return:
        """
        self.depth = depth
        self.variableCount = variableCount
        self.genotype = self.randomGrow(depth, variableCount)

    def randomGrow(self, depth, variableCount):
        """
            Randomly grows the function tree by either adding children, or by replacing tree branches.
        :param depth:
        :param variableCount:
        :return:
        """
        self.depth = depth
        self.variableCount = variableCount
        if depth == 0:          #leaf node
            rnd = random.random()
            if rnd < LEAF_CONSTANT_PROB:
                return [1.0]
            else:
                return [int(random.randint(0,variableCount - 1))]

        else:
            rnd = random.random()
            if rnd < MAKE_LEAF_PROB:
                return self.randomGrow(0, variableCount)
            else:
                operand = random.choice(BINARY_FUNCTIONS + UNARY_FUNCTIONS)
                if operand in BINARY_FUNCTIONS:
                    left = self.randomGrow(depth-1, variableCount)
                    right = self.randomGrow(depth-1, variableCount)
                    return [operand] + left + right
                elif operand in UNARY_FUNCTIONS:
                    left = self.randomGrow(depth-1, variableCount)
                    return [operand] + left

    def computeFunction(self, input, pos=0):
        """
            Computes the function given by the function tree memorized as a preorder in self.genotype
        :param input: the input variables
        :param pos: the starting index in the preorder list
        :return:
        """
        elem = self.genotype[pos]
        if isinstance(elem, float):
            return elem, pos+1
        elif isinstance(elem, int):
            return input[elem], pos+1
        elif elem in BINARY_FUNCTIONS:                              #compute the unary function(single operand)
            left, pos = self.computeFunction(input, pos + 1)
            right, pos = self.computeFunction(input, pos)

            if elem == '+':
                result = left + right
            elif elem == '-':
                result = left - right
            elif elem == '*':
                result = left * right
            elif elem == '/':
                if right == 0:
                    right = 1
                result = left / right
            elif elem == 'x^y':
                if left == 0:
                    left = 0.01
                result = left**(int(right))

            return result, pos

        elif elem in UNARY_FUNCTIONS:                               #compute the binary function(two operands)
            left ,pos= self.computeFunction(input, pos + 1)

            left = self.scale(left,-900000000,18446737095)

            if elem == 'sin':
                result = sin(left)
            elif elem == 'cos':
                result = cos(left)
            elif elem == 'e^':
                result =  exp(left)
            elif elem == '2^':
                result = 2**(int(left))
            elif elem == 'ln':
                left =  abs(left)
                if left < 0.1:
                    left = 0.1
                result =  log(abs(left))
            elif elem == 'tg':
                result = tangent(left)
            elif elem == 'arcsin':
                result =  arcsin(left)
            elif elem == 'arccos':
                result =  arccos(left)
            elif elem == 'tanh':
                result =  tanh(left)
            elif elem == 'abs':
                result =  abs(left)
            elif elem == 'sigmoid':
                left = self.scale(left,-5,5)
                result = 1/(1+ exp(-left))
            elif elem == 'x^x':
                result = left**left
            elif elem == 'int':
                result = int(left)
            elif elem == '-1^':
                result = (-1)**(int(left))

            result = self.scale(result, -900000000, 18446737095)
            return result, pos

    def eval(self, input, output):
        """
            Computes the mean squared error between the prediction and the actual value.
        :param input:
        :param output:
        :return:
        """
        error = 0
        for x,y in zip(input, output):
            pred = 0
            try:
                pred,_ = self.computeFunction(x)
                error += ((y - pred) ** 2)/2
            except RuntimeWarning :
                #print("error in pred " + str(y) + str(pred))
                self.genotype = []
                self.grow(self.depth, self.variableCount)
                self.eval(input, output)
            except OverflowError :
                #print("error in pred " + str(y) + str(pred))

                self.genotype = []
                self.grow(self.depth, self.variableCount)
                self.eval(input, output)



        error /= (len(input))
        self.phenotype = error

    def getDepth(self, pos=0):
        """
            Returns the depth of the function tree.
        :param pos:
        :return:
        """
        elem = self.genotype[pos]
        if isinstance(elem, float):
            return 1, pos+1
        elif isinstance(elem, int):
            return 1, pos+1
        elif elem in BINARY_FUNCTIONS:
            left, pos = self.getDepth(pos + 1)
            right, pos = self.getDepth(pos)

            return 1+max(left, right), pos

        elif elem in UNARY_FUNCTIONS:
            left ,pos= self.getDepth(pos + 1)

            return left+1, pos




















