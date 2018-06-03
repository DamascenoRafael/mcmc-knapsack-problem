import random
import copy
import numpy as np
import math
import gc
from datetime import datetime


class State():

    items = None
    v = 0
    w = 0

    def __init__(self):
        self.items = []
        self.v = 0
        self.w = 0

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
        obj_copy.v += self.v
        obj_copy.w += self.w
        return obj_copy

    def __repr__(self):
        return str(self.items)+","+str(self.v)+","+str(self.w)

    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self,other):
        return self.items == other.items
    
    def __gt__(self,other):
        return self.v > other.v

class Simulation():

    n = 0
    w = []
    v = []
    maxWeight = 0
    bestSolution = None
    currentSolution = None
    optimum = 0
    states = None

    def __init__(self,file):
        random.seed(datetime.now())
        self.n = 0
        self.w = []
        self.v = []
        self.bestSolution = None
        self.currentSolution = None
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

    def isValidStateWith(self,w,state = State()):
        if(len(state.items) == 0):
            state = self.currentSolution
        return state.w + w <= self.maxWeight

    def isBetterSolution(self,solution):
        return (solution.v > self.bestSolution.v) or (solution.v == self.bestSolution.v and solution.w < self.bestSolution.w)

    def newStates(self,state = State()):
        if(len(state.items) == 0 ):
            state = self.currentSolution.copy()

        possibleStates = []
        solution_i = State()
        for i in range(self.n):
            solution_i = state.copy()
            
            if solution_i.items[i] == 0:
                if self.isValidStateWith(self.w[i],state):
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
            if(p_ij<0):
                print(state,len(state.items),self.n)
        p.append(p_ii)
        return p[:]    
    
    def metropolisHasting(self):
        count = 0
        while(count<5000):
            count+=1
            possibleStates = self.newStates()
            prob = self.calculeteP(possibleStates)
            possibleStates.append(self.currentSolution.copy())
            newState = State()
            newState = np.random.choice(possibleStates,p=prob).copy()
            self.currentSolution = newState.copy()
            if self.isBetterSolution(self.currentSolution):
                self.bestSolution = self.currentSolution.copy()
                #print("itt =>",count,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
                if(self.bestSolution.v == self.optimum):
                    break
        return count

    def betterStatesThanCurrent(self, states):
        return [state for state in states if state.v > self.currentSolution.v]

    def hillClimbing(self):
        # bestSolution is always currentSolution
        count = 0
        while(1):
            count+=1
            newState = max(self.newStates())
            if self.isBetterSolution(newState):
                self.bestSolution = newState.copy()
                #print("FOUND BETTER: itt =>",count,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
            else:
                print("LOCAL MAX: itt =>",count-1,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
                break
        return count-1

    def calculate(self,solution):
        sum = 0
        for i in range(len(solution.items)):
            if(solution.items[i]):
                sum+= self.v[i]
        return sum        


if __name__ == '__main__':
    problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    # s = Simulation('TC/500_11.csv')
    # s.metropolisHasting()
    # print('best found',s.bestSolution.v,'\nbest calculated',s.calculate(s.bestSolution),'\nbest from file',s.optimum)
    for problem in problems:
        # values = []
        # values_itt = []
        # max_min = [0,math.inf]
        # itt_max_min = [0,math.inf]
        for i in range(50):
            print("Problem ",problem,"Simutaion ",i)
            s = Simulation('TC/'+problem)
            s.hillClimbing()
        #     itt = s.metropolisHasting()
        #     values.append(s.bestSolution.v)
        #     values_itt.append(itt)
        #     if(s.bestSolution.v>max_min[0]):
        #         max_min[0] = s.bestSolution.v
        #     if(s.bestSolution.v<max_min[1]):
        #         max_min[1] = s.bestSolution.v
        #     if(itt>itt_max_min[0]):
        #         itt_max_min[0] = itt
        #     if(itt<itt_max_min[1]):
        #         itt_max_min[1] = itt
        # print("=========================")
        # print('Problem Optimal :: ',s.optimum)
        # print("Optimal :: ",itt_max_min[0],"Worse :: ",itt_max_min[1])
        # print('Mean Optimal :: ',np.median(values))
        # print('Variance Optimal :: ',np.var(values))
        # print("=========================")
        # print("Max itt :: ",itt_max_min[0],"Min itt :: ",itt_max_min[1])
        # print('Mean itt :: ',np.median(values_itt))
        # print('Variance  itt :: ',np.var(values_itt))
        # print("=========================")


   