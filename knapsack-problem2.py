import random
import copy
import numpy as np
from datetime import datetime


class State():

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

    def copy(self):
        obj_copy = State()
        obj_copy.items = self.items[:]
        obj_copy.v = self.v
        obj_copy.w = self.w
        return obj_copy

    def __repr__(self):
        return str(self.items)+","+str(self.v)+","+str(self.w)

    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self,other):
        return self.items == other.items

class Simulation():

    n = 0
    w = []
    v = []
    maxWeight = 0
    bestSolution = None
    currentSolution = None
    optimum = 0
    states = {}

    def __init__(self,file):
        random.seed(datetime.now())
        print("Reading File...")
        
        with open(file) as f:
            self.n = int(f.readline().split()[1])
            self.maxWeight = int(f.readline().split()[1])
            self.optimum = int(f.readline().split()[1])
            f.readline()
            self.currentSolution = State()
            self.bestSolution = State() 
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
        self.bestSolution = self.currentSolution.copy()
        print("File Read")

    def isValidStateWith(self,w):
        return self.currentSolution.w + w <= self.maxWeight

    def isBetterSolution(self,solution):
        return (solution.v > self.bestSolution.v) or (solution.v == self.bestSolution.v and solution.w < self.bestSolution.w)

    def newStates(self):
        possibleStates = []
        for i in range(self.n):
            solution_i = State()
            solution_i = self.currentSolution.copy()
            
            if solution_i.items[i] == 0:
                if self.isValidStateWith(self.w[i]):
                    solution_i.setIn(i,self.v[i],self.w[i])
                    possibleStates.append(solution_i.copy())
            else:
                solution_i.setOut(i,self.v[i],self.w[i])
                possibleStates.append(solution_i.copy())
        return possibleStates[:]

    def randomWalk(self,p):
        print("Max",self.maxWeight)
        count = 0
        while(count<10000):
            count += 1
            unif = random.random()
            if unif < p:
                possibleStates = self.newStates()
                index = random.randint(0, len(possibleStates)-1)
                newState = State()
                newState = possibleStates[index].copy()
                self.currentSolution = newState.copy()
                if self.isBetterSolution(self.currentSolution):
                    self.bestSolution = self.currentSolution.copy()
                    print("Best  V =>",self.bestSolution.v,self.bestSolution.w)

    def accept(self,newState):
        unif = random.random()
        alfa = (newState['v']*math.log(currentSolution['w'])) / (currentSolution['v']*math.log(newState['w']))
        #alfa = (newState['v'])/(currentSolution['v'])
        if(unif < alfa ):
            return True
        return False

    def calculeteP(self,states):
        p = []
        p_ii = 1
        currentV = self.currentSolution.v
        for state in states:
            p_ij = min(1,state.v/currentV)/(len(states))
            p.append(p_ij)
            p_ii -= p_ij
        p.append(p_ii)
        return p[:]    
    
    def metropolisHasting(self):
        count = 0
        while(count<5000):
            count+=1
            possibleStates = None
            prob = None
            if (self.currentSolution in self.states):
                possibleStates,prob = self.states[self.currentSolution]
            else:
                possibleStates = self.newStates()
                prob = self.calculeteP(possibleStates)
                possibleStates.append(self.currentSolution.copy())
                self.states[self.currentSolution] = [possibleStates[:],prob[:]]                           
            newState = State()
            newState = np.random.choice(possibleStates,p=prob).copy()
            self.currentSolution = newState.copy()
            if self.isBetterSolution(self.currentSolution):
                self.bestSolution = self.currentSolution.copy()
                print("itt =>",count,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
                    


if __name__ == '__main__':
    #problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    #for problem in problems
    #    s = Simulation('TC/'+problem)
    #    s.metropolisHasting()
    #    print(s.optimum,s.maxWeight)
    s = Simulation("TC/500_11.csv")
    s.metropolisHasting()
