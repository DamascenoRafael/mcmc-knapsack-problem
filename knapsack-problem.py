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
    with open(name) as f:
        n = f.readline()
        maxWeight = map(int, f.readline().split())[1]
        optimum = map(int, f.readline().split())[1]
        f.readline() # time
        for line in f:
            _, lineV, lineW, _ = map(int, line.split(','))
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
    return currentSolution['w'] + lineW <= maxWeight

def addItem(item, solution):
    solution['items'][item] = 1
    solution['w'] += w[item]
    solution['v'] += v[item]

def removeItem(item, solution):
    solution['items'][item] = 0
    solution['w'] -= w[item]
    solution['v'] -= v[item]

def newStates():
    possibleStates = []
    # gerar aleatorio
    # ver qual o vértice
    # ver se ele já está na sol
    # se tiver retiro
    # se não tiver vejo se pode ser adicionado
    for i in range(n):
        solution_i = currentSolution.copy()
        if solution_i['items'][i] == 0:
            if isValidStateWith(w[i]):
                addItem(i, solution_i)
                possibleStates.append(solution_i.copy())
        else:
            removeItem(i, solution_i)
            possibleStates.append(solution_i.copy())
    
    return possibleStates


def currentValue():
    pass

def currentWeight():
    pass

def remainingWeight():
    pass
    #return maxWeight - currentWeight()