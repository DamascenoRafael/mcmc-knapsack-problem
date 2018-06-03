from simulation import *

if __name__ == '__main__':
    #problems = ['500_11.csv']
    problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    for problem in problems:
        values = []
        values_itt = []
        max_min = [0,math.inf]
        itt_max_min = [0,math.inf]

        for i in range(50):
            print("Problem ",problem,"Simutaion ",i)
            s = Simulation('../data/'+problem)
            
            #itt = s.randomWalk(1)
            #itt = s.randomWalk(0.5)
            #itt = s.metropolisHasting()
            itt = s.hillClimbing()

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
        print("Optimal :: ",itt_max_min[0],"Worse :: ",itt_max_min[1])
        print('Mean Optimal :: ',np.median(values))
        print('Variance Optimal :: ',np.var(values))
        print("=========================")
        print("Max itt :: ",itt_max_min[0],"Min itt :: ",itt_max_min[1])
        print('Mean itt :: ',np.median(values_itt))
        print('Variance  itt :: ',np.var(values_itt))
        print("=========================")