import math
from simulation import *

if __name__ == '__main__':
    problems = ['500_11.csv']
    #problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    times = 2
    for problem in problems:
        res = []
        for i in range(times):
            s = Simulation('../data/'+problem)
            
            #itt = s.randomWalk(1)
            #itt = s.randomWalk(0.5)
            out = s.metropolisHasting()
            #itt = s.hillClimbing()
            #itt, temperature = s.simulatedAnnealing(10**4, 10**(-8), s.linearCoolingStrategy, 0.5)
            #itt, temperature = s.simulatedAnnealing(10**30, 10**(-8), s.expCoolingStrategy, 0.99)
            #itt, temperature = s.simulatedAnnealing(10**5, 10**(-8), s.dynamicCoolingStrategy, 0.5)
            res.append(out)
        with open("../data/"+problem+".out",'w') as f:
            print("writting")
            f.write(str(s.optimum)+"\n")
            array =  np.zeros(len(res[0]))
            for i in res:
                array += np.array(i)
            array = array/times
            for i in array:
                f.write(str(i)+',')
            print("end writting")
