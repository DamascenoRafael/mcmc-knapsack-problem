import random
import numpy as np
from datetime import datetime
from state import *
from math import exp,log

class Simulation():

    n = 0
    w = []
    v = []
    maxWeight = 0
    bestSolution = None
    currentSolution = None
    optimum = 0
    prob = {}
    executions = 10**4

    def __init__(self,file):
        random.seed(datetime.now())
        self.n = 0
        self.w = []
        self.v = []
        self.bestSolution = None
        self.currentSolution = None
        prob = None
        prob = {}
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

    def allNewStates(self,state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()

        possibleStates = []
        for i in range(self.n):
            new = State()
            new = self.newStateFor(i, state)
            if len(new.items) != 0:
                possibleStates.append(new.copy())
        return possibleStates[:]
    
    def newStateFor(self, i, state = State()):
        if len(state.items) == 0:
            state = self.currentSolution.copy()
        
        state_i = State()
        state_i = state.copy()
        if state_i.items[i] == 0:
            if self.isValidStateWith(self.w[i], state):
                state_i.setIn(i, self.v[i], self.w[i])
                return state_i
        else:
            state_i.setOut(i, self.v[i], self.w[i])
            return state_i
    
        return State()

    def randomWalk(self,p):
        print("Max",self.maxWeight)
        count = 0
        while(count<self.executions):
            count += 1
            unif = random.random()
            if unif < p:
                possibleStates = self.allNewStates()
                index = random.randint(0, len(possibleStates)-1)
                newState = State()
                newState = possibleStates[index].copy()
                self.currentSolution = newState.copy()
                if self.isBetterSolution(self.currentSolution):
                    self.bestSolution = self.currentSolution.copy()
                    break
            ret.append(self.bestSolution.v)

        if(count<self.executions):
            for i in range(count,self.executions):
                ret.append(self.bestSolution.v)
        return ret


    def accept(self,newState, pij, pji):
        unif = random.random()
        # alfa = (newState.v*math.log(self.currentSolution.w)) / (currentSolution.v*math.log(newState.w))
        alfa = (newState.v * pji) / (self.currentSolution.v * pij)
        if unif < alfa:
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
        ret =[]
        while(count<self.executions):
            count += 1
            currentChanged = False
            newState = State()
            while (len(newState.items) == 0):
                index = random.randint(0, self.n-1)
                newState = self.newStateFor(index).copy()
            # possibleStates = self.allNewStates()
            # prob = self.calculeteP(possibleStates)
            #possibleStates.append(self.currentSolution.copy())
            #newState = State()
            #newState = np.random.choice(possibleStates,p=prob).copy()

            delta = newState.v - self.currentSolution.v
            if delta > 0:
                # accept = 1
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                
                pij = self.prob.setdefault(self.currentSolution, None)
                if pij == None:
                    pij = 1 / len(self.allNewStates())
                    self.prob[self.currentSolution] = pij
                
                pji = self.prob.setdefault(newState, None)
                if pji == None:
                    pji = 1 / len(self.allNewStates(newState))
                    self.prob[newState] = pji
                if self.accept(newState, pij, pji):
                    self.currentSolution = newState.copy()
                    currentChanged = True
            if currentChanged and self.isBetterSolution(self.currentSolution):
                self.bestSolution = self.currentSolution.copy()
                if(self.bestSolution.v == self.optimum):
                    break
            ret.append(self.bestSolution.v)

        if(count<self.executions):
            for i in range(count,self.executions):
                ret.append(self.bestSolution.v)
        return ret

    def hillClimbing(self):
        # bestSolution is always currentSolution
        count = 0
        ret = []
        while(1):
            count+=1
            newState = max(self.allNewStates())
            if self.isBetterSolution(newState):
                self.bestSolution = newState.copy()
                #print("FOUND BETTER: itt =>",count,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
                ret.append(self.bestSolution.v)
            else:
                print("LOCAL MAX: itt =>",count-1,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
                break

        if(count<self.executions):
            for i in range(count,self.executions):
                ret.append(self.bestSolution.v)
        return ret
    
    def boltzman(self, deltaV, t, pij, pji):
        return exp(deltaV/t) * pji / pij

    def simulatedAnnealing(self, initialT, epsilon, coolingStrategy, beta):
        t = 0
        temperature = initialT
        ret = []
        while(temperature > epsilon):
            t+=1
            currentChanged = False
            # possibleStates = self.allNewStates()
            # newState = State()
            # newState = np.random.choice(possibleStates).copy()
            newState = State()
            while (len(newState.items) == 0):
                index = random.randint(0, self.n-1)
                newState = self.newStateFor(index).copy()
            delta = newState.v-self.currentSolution.v
            if delta > 0:
                # boltzman = 1
                self.currentSolution = newState.copy()
                currentChanged = True
            else:
                pij = self.prob.setdefault(self.currentSolution, None)
                if pij == None:
                    pij = 1 / len(self.allNewStates())
                    self.prob[self.currentSolution] = pij
                
                pji = self.prob.setdefault(newState, None)
                if pji == None:
                    pji = 1 / len(self.allNewStates(newState))
                    self.prob[newState] = pji
    
                    
                if random.random() < self.boltzman(delta, temperature, pij, pji):
                    self.currentSolution = newState.copy()
                    currentChanged = True

            if currentChanged and self.isBetterSolution(self.currentSolution):
                self.bestSolution = self.currentSolution.copy()
                #print("itt =>",t,"- Best  V =>",self.bestSolution.v,"W =>",self.bestSolution.w)
                if(self.bestSolution.v == self.optimum):
                    break
                    
            ret.append(self.bestSolution.v)
            temperature = coolingStrategy(initialT, beta, t, delta)

        if(t<self.executions):
            for i in range(t,self.executions):
                ret.append(self.bestSolution.v)
        return ret
        

    def linearCoolingStrategy(self, initialT, beta, t, delta):
        return initialT-beta*t

    def expCoolingStrategy(self, initialT, beta, t, delta):
        return initialT*(beta**t)

    def dynamicCoolingStrategy(self, initialT, beta, t, delta):
        return initialT-beta*t - (log(abs(delta))/delta)*t

    def verifyValues(self,solution):
        sum = 0
        for i in range(len(solution.items)):
            if(solution.items[i]):
                sum+= self.v[i]
        return sum