import random
import copy
import numpy as np
import time
import math

n = 0
w = []
v = []

maxWeight = 0
optimum = 0

currentSolution = {}

bestSolution = {}

def readProblemFrom(name):
    global n, maxWeight, optimum, bestSolution,currentSolution,w,v
    w = []
    v = []
    currentSolution = {
    'items': [],
    'v': 0,
    'w': 0,
    'itt':0
    }

    bestSolution = {
        'items': [],
        'v': 0,
        'w': 0,
        'itt':0,
    }

    with open(name) as f:
        n = int(f.readline().split()[1])
        maxWeight = int(f.readline().split()[1])
        optimum = int(f.readline().split()[1])
        f.readline() # time
        for line in f:
            _, lineV, lineW, _ = list(map(int, line.split(',')))
            v.append(lineV)
            w.append(lineW)
            if random.random() < 0.5 and isValidStateWith(lineW):
                currentSolution['items'].append(1)
                currentSolution['v'] += lineV
                currentSolution['w'] += lineW
            else:
                currentSolution['items'].append(0)
        bestSolution = copy.deepcopy(currentSolution)

def isValidStateWith(w):
    return currentSolution['w'] + w <= maxWeight

def addItem(item, solution):
    solution['items'][item] = 1
    solution['w'] += w[item]
    solution['v'] += v[item]
    return copy.deepcopy(solution)

def removeItem(item, solution):
    solution['items'][item] = 0
    solution['w'] -= w[item]
    solution['v'] -= v[item]
    return copy.deepcopy(solution)

def isBetterSolution(solution):
    return (solution['v'] > bestSolution['v']) or (solution['v'] == bestSolution['v'] and solution['w'] < bestSolution['w'])

def allNewStates():
    start = time.time()
    possibleStates = []
    for i in range(n):
        new = newStateFor(i)
        if new != None:
            possibleStates.append(copy.deepcopy(new))
    print("states",time.time()-start)
    return possibleStates

def newStateFor(i):
    global currentSolution
    solution_i = copy.deepcopy(currentSolution)
    if solution_i['items'][i] == 0:
        if isValidStateWith(w[i]):
            solution_i = addItem(i, solution_i)
            return solution_i
    else:
        solution_i = removeItem(i, solution_i)
        return solution_i
    
    return None

def randomWalk(p):
    global bestSolution, currentSolution
    count = 0
    while(count<500):
        count += 1
        unif = random.random()
        if unif < p:
            newState = None
            while (newState == None):
                index = random.randint(0, n-1)
                newState = newStateFor(index)
            currentSolution = copy.deepcopy(newState)
            if isBetterSolution(currentSolution):
                bestSolution = copy.deepcopy(currentSolution)
                print('best: ', bestSolution['v'], '    i:', count)
                bestSolution['itt']=count

    print("best",bestSolution,"\ncurr",currentSolution,"\nOpt",optimum)



def accept(newState):
    global currentSolution
    unif = random.random()
    alfa = (newState['v']*math.log(currentSolution['w'])) / (currentSolution['v']*math.log(newState['w']))
    #alfa = (newState['v'])/(currentSolution['v'])
    if(unif < alfa ):
        return True
    return False      
    
def metropolisHasting():
    global currentSolution, bestSolution
    count = 0
    while(count<5000):
        count+=1
        newState = None
        while (newState == None):
            index = random.randint(0, n-1)
            newState = newStateFor(index)
        if( accept(newState)):
            currentSolution = copy.deepcopy(newState)
            if(isBetterSolution(currentSolution)):
                bestSolution = copy.deepcopy(currentSolution)
                #print('best: ', bestSolution['v'], '    i:', count)
                bestSolution['itt']=count
                if(bestSolution['v']==optimum):
                    break
    #print("best",bestSolution['v'],"\ncurr",currentSolution['v'],"\nOpt",optimum)

problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']

for problem in problems:
    values = []
    values_itt = []
    for i in range(50):
        print(problem,i)
        readProblemFrom("TC/"+problem)
        metropolisHasting()
        values.append(bestSolution['v'])
        values_itt.append(bestSolution['itt'])

    print("\n",problem)
    print('Problem Optimal :: ',optimum)
    print('Mean Optimal :: ',np.median(values))
    print('Variance Optimal :: ',np.var(values))
    print('Mean itt :: ',np.median(values_itt))
    print('Variance  itt :: ',np.var(values_itt))

