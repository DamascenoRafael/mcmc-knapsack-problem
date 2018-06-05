import math
from simulation import *

if __name__ == '__main__':
    problems = ['500_11.csv']
    #problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    for problem in problems:
        values = []
        values_itt = []
        max_min = [0,math.inf]
        itt_max_min = [0,math.inf]

        for i in range(1):
            print("Problem ",problem,"Simutaion ",i)
            s = Simulation('../data/'+problem)
            
            #itt = s.randomWalk(1)
            #itt = s.randomWalk(0.5)
            itt = s.metropolisHasting()
            #itt = s.hillClimbing()
            #itt, temperature = s.simulatedAnnealing(10**4, 10**(-8), s.linearCoolingStrategy, 0.5)
            #itt, temperature = s.simulatedAnnealing(10**30, 10**(-8), s.expCoolingStrategy, 0.99)
            #itt, temperature = s.simulatedAnnealing(10**5, 10**(-8), s.dynamicCoolingStrategy, 0.5)

            print('Last Temp:',temperature)

            values.append(s.bestSolution.v)
            values_itt.append(itt)
            if(s.bestSolution.v>max_min[0]):
                max_min[0] = s.bestSolution.v
            if(s.bestSolution.v<max_min[1]):
                max_min[1] = s.bestSolution.v
            if(itt>itt_max_min[0]):
                itt_max_min[0] = itt
            if(itt<itt_max_min[1]):
                itt_max_min[1] = itt

        print("=========================")
        print('Problem Optimal :: ',s.optimum)
        print("=========================")
        print("Optimal :: ",max_min[0],"Worse :: ",max_min[1])
        print('Mean Optimal :: ',np.mean(values))
        print('Variance Optimal :: ',np.var(values))
        print("=========================")
        print("Max itt :: ",itt_max_min[0],"Min itt :: ",itt_max_min[1])
        print('Mean itt :: ',np.mean(values_itt))
        print('Variance  itt :: ',np.var(values_itt))
        print("=========================")