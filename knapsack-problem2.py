import random
import copy
from datetime import datetime


class Solution():

    items = []
    v = 0
    w = 0

    def setIn(self,index,v,w):
        if(self.items[index]!=1):
            self.items[index] = 1
            self.w += w
            self.v += v
        return self

    def setOut(self,index,v,w):
        if(self.items[index]!=0):
            self.items[index] = 0
            self.w -= w
            self.v -= v
        return self
    def __repr__(self):
        return "Items: "+str(self.items)+ " Value: "+str(self.v)+" Weight: "+str(self.w)

class Simulation():

    n = 0
    w = []
    v = []
    maxWeight = 0
    bestSolution = None
    currentSolution = None
    optimum = 0

    def __init__(self,file):
        random.seed(datetime.now())
        print("Reading File...")
        
        with open(file) as f:
            self.n = int(f.readline().split()[1])
            self.maxWeight = int(f.readline().split()[1])
            self.optimum = int(f.readline().split()[1])
            f.readline()
            self.currentSolution = Solution()
            for line in f:
                _, lineV, lineW, _ = list(map(int, line.split(',')))
                self.v.append(lineV)
                self.w.append(lineW)
                if random.random() < 0.5 and self.isValidStateWith(lineW):
                    self.currentSolution.items.append(1)
                    self.currentSolution.v += lineV
                    self.currentSolution.w += lineW
                else:
                    self.currentSolution.items.append(0)
        self.bestSolution = copy.deepcopy(self.currentSolution)
        print("File Read")

    def isValidStateWith(self,w):
        return self.currentSolution.w + w <= self.maxWeight

    def isBetterSolution(self,solution):
        return (solution.v > self.bestSolution.v) or (solution.v == self.bestSolution.v and solution.w < self.bestSolution.w)

    def newStates(self):
        possibleStates = []
        for i in range(self.n):
            solution_i = Solution()
            solution_i.items = copy.deepcopy(self.currentSolution.items)
            solution_i.v = copy.deepcopy(self.currentSolution.v)
            solution_i.w = copy.deepcopy(self.currentSolution.w)
            
            if solution_i.items[i] == 0:
                if self.isValidStateWith(self.w[i]):
                    solution_i = copy.deepcopy(solution_i.setIn(i,self.v[i],self.w[i]))
                    possibleStates.append(copy.deepcopy(solution_i))
            else:
                solution_i = copy.deepcopy(solution_i.setOut(i,self.v[i],self.w[i]))
                possibleStates.append(copy.deepcopy(solution_i))

        return copy.deepcopy(possibleStates)

    def lazyRandomWalk(self):
        print("Max",self.maxWeight)
        count = 0
        while(count<50000):
            count += 1
            unif = random.random()
            if unif < 0.5:
                possibleStates = copy.deepcopy(self.newStates())
                index = random.randint(0, len(possibleStates)-1)
                newState = copy.deepcopy(possibleStates[index])
                self.currentSolution = copy.deepcopy(newState)
                if self.isBetterSolution(self.currentSolution):
                    self.bestSolution = copy.deepcopy(self.currentSolution)
                    print("New Best Solution ",self.bestSolution.v,self.bestSolution.w)

if __name__ == '__main__':
    s = Simulation('teste2.csv')
    print(s.optimum)
    s.lazyRandomWalk()
