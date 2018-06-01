import random

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
        bestSolution = currentSolution.copy()

def isValidStateWith(w):
    return currentSolution['w'] + w <= maxWeight

def addItem(item, solution):
    solution['items'][item] = 1
    solution['w'] += w[item]
    solution['v'] += v[item]
    return solution.copy()

def removeItem(item, solution):
    solution['items'][item] = 0
    solution['w'] -= w[item]
    solution['v'] -= v[item]
    return solution.copy()

def isBetterSolution(solution):
    return (solution['v'] > bestSolution['v']) or (solution['v'] == bestSolution['v'] and solution['w'] < bestSolution['w'])

def newStates():
    global currentSolution
    possibleStates = []
    for i in range(n):
        solution_i = currentSolution.copy()
        if solution_i['items'][i] == 0:
            if isValidStateWith(w[i]):
                solution_i = addItem(i, solution_i)
                possibleStates.append(solution_i.copy())
        else:
            solution_i = removeItem(i, solution_i)
            possibleStates.append(solution_i.copy())
    
    return possibleStates

def lazyRandomWalk():
    global bestSolution, currentSolution
    count = 0
    while(count<10):
        count += 1
        unif = random.random()
        if unif < 0.5:
            possibleStates = newStates()
            index = random.randint(0, len(possibleStates)-1)
            newState = possibleStates[index]
            currentSolution = newState.copy()
            if isBetterSolution(currentSolution):
                bestSolution = currentSolution.copy()


readProblemFrom('teste.csv')
lazyRandomWalk()
