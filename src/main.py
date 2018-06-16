import os
import math
from enum import Enum
from simulation import *
import matplotlib.pyplot as plt

dataFolder = '../data/'
outputFolder = '../output/'

algorithms = []
algorithms_params = []

class Algorithm(Enum):
    randomWalk = 1
    metropolisHasting = 2
    hillClimbing = 3
    simulatedAnnealing = 4

class CoolingStrategy(Enum):
    linear = 1
    exp = 2
    dynamic = 3

def cleanOutputFolder():
    filelist = [ f for f in os.listdir(outputFolder) ]
    for f in filelist:
        os.remove(os.path.join(outputFolder, f))

def addAlgorithm(alg, *params):
    global algorithms, algorithms_params

    algorithms.append(alg.value)
    algorithms_params.append(params)

def execute(problems, executions, times, mean):
    global algorithms, algorithms_params
    
    for problem in problems:
        s = Simulation(dataFolder + problem, executions)

        for x in range(len(algorithms)):
            res = []
            bestFound = 0
            name = ''
            alg = algorithms[x]
            alg_params = algorithms_params[x]

            for i in range(times):
                s = Simulation(dataFolder + problem, executions)
                if alg == 1:
                    name, out = s.randomWalk(alg_params[0])
                elif alg == 2:
                    name, out = s.metropolisHasting()
                elif alg == 3:
                    name, out = s.hillClimbing()
                else:
                    strategyIndex = alg_params[2].value
                    if strategyIndex == 1:
                        coolingStrategy = s.linearCoolingStrategy
                    elif strategyIndex == 2:
                        coolingStrategy = s.expCoolingStrategy
                    else:
                        coolingStrategy = s.dynamicCoolingStrategy
                    name, out = s.simulatedAnnealing(alg_params[0], alg_params[1], coolingStrategy, alg_params[3])

                if mean and times > 1:
                    res.append(out)
                else:
                    if s.bestSolution.v > bestFound:
                        res = out
                        bestFound = s.bestSolution.v

            if mean and times > 1:
                max_size = max([len(res[i]) for i in range(len(res))])
                vec_sum = np.zeros(max_size)
                for v in res:
                    v.extend([v[-1] for i in range(max_size-len(v))])
                    vec_sum += np.array(v)
                vec_sum /= len(res)
                res = vec_sum.tolist()
                name = str(times) + '_times_mean_' + name

            saveResult(res, problem, name, s.optimum)

def saveResult(result, problem, algorithmName, optimum):
    fileName = outputFolder + problem + '.out'
    new = False

    if not os.path.exists(fileName):
        new = True
        os.makedirs(os.path.dirname(fileName), exist_ok=True)

    with open(fileName, 'a') as f:
        print('writting', problem, algorithmName)
        if not new:
            f.write('\n')
        f.write(str(optimum) + ',')
        f.write(algorithmName + ',')
        result = ','.join(map(str, result)) 
        f.write(result)

def plotComparison(problems, gType = 'std'):
    for problem in problems:
        print('Plotting opt value graphic', problem)
        plt.figure(figsize=(16,9))
        fileName = outputFolder + problem + '.out'
        opt = 0
        with open(fileName) as file:
            for line in file:
                splittedLine = line.split(',')
                opt = float(splittedLine[0])
                algorithmName = str(splittedLine[1])
                splittedResults = list(map(lambda x: float(x), splittedLine[2:]))
                if(gType=="log"):
                    plt.loglog(range(1,1+len(splittedResults)), splittedResults, label=algorithmName)
                else:
                    plt.plot(range(len(splittedResults)), splittedResults, label=algorithmName)

        plt.axhline(y=opt, linestyle='dashed', color='c')
        plt.legend()
        plt.xlabel('Steps')
        plt.ylabel('Values in knapsack')
        plt.savefig(outputFolder + problem + '_' + gType + '_values.png')
        plt.clf()

def plotError(problems, gType = 'std'):
    for problem in problems:
        print('plotting error graphic', problem)
        plt.figure(figsize=(16,9))
        fileName = outputFolder + problem + '.out'
        opt = 0
        with open(fileName) as file:
            for line in file:
                splittedLine = line.split(',')
                opt = float(splittedLine[0])
                algorithmName = str(splittedLine[1])
                splittedResults = list(map(lambda x: abs(float(x)-opt), splittedLine[2:]))
                if(gType=="log"):
                    plt.loglog(range(1,1+len(splittedResults)), splittedResults, label=algorithmName)
                else:
                    plt.plot(range(len(splittedResults)), splittedResults, label=algorithmName)
        
        plt.legend()
        plt.xlabel('Steps')
        plt.ylabel('Error')
        plt.savefig(outputFolder + problem + '_' + gType + '_error.png')
        plt.clf()


if __name__ == '__main__':

    executions = 10 ** 4            # number of iterations for the algorithms (except Simulated Annealing)
    times = 3                       # how many times each algorithm will be executed
    mean = True                     # mean or optimum result to be saved and plotted

    cleanOutputFolder()

    # ploblems that will be executed
    problems = ['test1.csv', 'test5.csv']

    # algorithms that will be executed for each problem
    # - randomWalk receives the parameter 'p'
    # - metropolisHasting and hillClimbing do not receive parameters
    # - simulatedAnnealing receives the parameters 'initialT', 'epsilon', 'coolingStrategy' and 'beta'
    addAlgorithm(Algorithm.randomWalk, 0.5)
    addAlgorithm(Algorithm.metropolisHasting)
    addAlgorithm(Algorithm.hillClimbing)
    addAlgorithm(Algorithm.simulatedAnnealing, 10**3, 10**(-8), CoolingStrategy.linear, 0.99)

    # solve problems
    execute(problems, executions, times, mean)

    # plot results
    plotComparison(problems, 'log')     # you can use without the 'log' parameter to plot the std
    plotError(problems, 'log')          # you can use without the 'log' parameter to plot the std