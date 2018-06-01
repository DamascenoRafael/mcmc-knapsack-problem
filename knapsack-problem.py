import random
import copy

n = 0
w = []
v = []

maxWeight = 0
optimum = 0

solution = {
    'items': [],
    'v': 0,
    'w': 0
}

currentSolution = {
    'items': [],
    'v': 0,
    'w': 0
}

bestSolution = {
    'items': [],
    'v': 0,
    'w': 0
}

def readProblemFrom(name):
    global n, maxWeight, optimum, bestSolution
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
    possibleStates = []
    for i in range(n):
        new = newStateFor(i)
        if new != None:
            possibleStates.append(copy.deepcopy(new))
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
    while(count<50000):
        count += 1
        unif = random.random()
        if unif < p:
            newState = None
            while (newState == None):
                index = random.randint(0, n-1)
                newState = newStateFor(index)
            currentSolution = copy.deepcopy(newState)
            if isBetterSolution(currentSolution):
                print('best: ', bestSolution['v'], '    i:', count)
                bestSolution = copy.deepcopy(currentSolution)


readProblemFrom('teste2.csv')
print('opti: ', optimum)
randomWalk(1)
print('opti: ', optimum)
