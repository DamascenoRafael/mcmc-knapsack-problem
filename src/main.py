import os
import math
from simulation import *
import matplotlib.pyplot as plt

dataFolder = '../data/'
outputFolder = '../output/'

def saveResult(result, problem, algorithmName):
    fileName = outputFolder + problem + '.out'
    if os.path.exists(fileName) :
        with open(fileName, 'a') as f:
            print('writting', problem, algorithmName)
            f.write('\n')
            f.write(str(s.optimum) + ',')
            f.write(algorithmName + ',')
            result = ','.join(map(str, result)) 
            f.write(result)
    else:
        os.makedirs(os.path.dirname(fileName), exist_ok=True)
        with open(fileName, 'w') as f:
            print('writting', problem, algorithmName)
            f.write(str(s.optimum) + ',')
            f.write(algorithmName + ',')
            result = ','.join(map(str, result)) 
            f.write(result)

def plotComparison(problems, gType="std"):
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

def plotError(problems, gType="std"):
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
    
    # ploblems that will be executed
    problems = ['teste.csv']

    for problem in problems:
        s = Simulation(dataFolder + problem, executions)
        res = []
        bestFound = 0
        name = ''
        for i in range(times):
            # name, out = s.randomWalk(1)
            # name, out = s.randomWalk(0.5)
            # name, out = s.metropolisHasting()
            # name, out = s.hillClimbing()
            # name, out = s.simulatedAnnealing(10**3, 10**(-8), s.linearCoolingStrategy, 0.99)
            name, out = s.simulatedAnnealing(10**20, 10**(-8), s.expCoolingStrategy, 0.99)
            # name, out = s.simulatedAnnealing(10**5, 10**(-8), s.dynamicCoolingStrategy, 0.5)
            
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
        
        saveResult(res, problem, name)

    # plotComparison(problems)
    plotComparison(problems,'log')    
    # plotError(problems)
    plotError(problems,'log')