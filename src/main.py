import os
import math
from simulation import *
import matplotlib.pyplot as plt

dataFolder = '../data/'
outputFolder = '../output/'

def saveResult(result, problem, algorithmName):
    fileName = outputFolder + problem + '.out'
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    with open(fileName, 'w') as f:
        print('writting', problem, algorithmName)
        f.write(str(s.optimum) + ',')
        f.write(algorithmName + ',')
        result = ','.join(map(str, result)) 
        f.write(result)

def plotComparison(problems):
    for problem in problems:
        print('plotting', problem)
        plt.figure(figsize=(16,9))
        fileName = outputFolder + problem + '.out'
        opt = 0
        with open(fileName) as file:
            for line in file:
                splittedLine = line.split(',')
                opt = float(splittedLine[0])
                algorithmName = str(splittedLine[1])
                splittedResults = list(map(lambda x: float(x), splittedLine[2:]))
                plt.loglog(range(len(splittedResults)), splittedResults, label=algorithmName)
        
        plt.axhline(y=opt, linestyle='dashed', color='c')
        plt.legend()
        plt.xlabel('Steps')
        plt.ylabel('Values in knapsack')
        plt.savefig(outputFolder + problem + '.png')
        plt.clf()


if __name__ == '__main__':
    problems = ['500_11.csv']
    times = 1

    for problem in problems:
        s = Simulation(dataFolder + problem, 10 ** 4)
        res = []
        bestFound = 0
        name = ''
        for i in range(times):
            # name, out = s.randomWalk(1)
            # name, out = s.randomWalk(0.5)
            # name, out = s.metropolisHasting()
            # name, out = s.hillClimbing()
            name, out = s.simulatedAnnealing(10**3, 10**(-8), s.linearCoolingStrategy, 0.99)
            # name, out = s.simulatedAnnealing(10**30, 10**(-8), s.expCoolingStrategy, 0.99)
            # name, out = s.simulatedAnnealing(10**5, 10**(-8), s.dynamicCoolingStrategy, 0.5)
            
            if s.bestSolution.v > bestFound:
                res = out
                bestFound = s.bestSolution.v
                
        saveResult(res, problem, name)

    plotComparison(problems)