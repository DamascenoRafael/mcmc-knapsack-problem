from simulation import *
import time

def knapSack(W, wt, val, n):
    start = time.time()

    K = [[0 for x in range(W+1)] for x in range(n+1)]
 
    # Build table K[][] in bottom up manner
    for i in range(n+1):
        for w in range(W+1):
            if i==0 or w==0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
 
    return K[n][W], time.time() - start


if __name__ == '__main__':
    problems = ['500_11.csv']
    # problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    # problems = ['teste2.csv']

    values = []

    for problem in problems:
        for i in range(1):
            print("Problem ",problem,"Simutaion ",i)
            s = Simulation('../data/'+problem)
            
            result, time = knapSack(s.maxWeight, s.w, s.v, s.n)
            print(result)
            values.append(time)
            