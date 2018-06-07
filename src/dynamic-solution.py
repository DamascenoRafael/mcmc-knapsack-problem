from simulation import *
import time

def dynamic(maxWeight, w, v, n):
    start = time.time()

    K = [[0 for x in range(maxWeight+1)] for x in range(n+1)]
 
    # Build table K[][] in bottom up manner
    for i in range(n + 1):                  # i first items allowed
        for j in range(maxWeight + 1):      # j max wight allowed
            if i == 0 or j == 0:
                K[i][j] = 0
            elif w[i-1] <= j:
                K[i][j] = max(v[i-1] + K[i-1][j-w[i-1]],  K[i-1][j])
            else:
                K[i][j] = K[i-1][j]

    best = K[n][maxWeight]
    elapsed = time.time() - start
    return best, elapsed

def evaluateDynamic(problem, times):
    values = []
    for i in range(times):
        # print('Problem', problem, 'Simutaion', i)
        s = Simulation('../data/' + problem)
        result, elapsedTime = dynamic(s.maxWeight, s.w, s.v, s.n)
        # print('Optimum was:', s.optimum, 'Found:', result)
        values.append(elapsedTime)
    meanTime = np.mean(values)
    print('Problem:', problem, 'Mean time:', meanTime)
    return meanTime

if __name__ == '__main__':
    problems = ['500_11.csv']
    # problems = ['500_11.csv','500_12.csv','500_13.csv','500_14.csv','500_15.csv','500_16.csv']
    # problems = ['teste2.csv']
    # problems = ['teste3.csv']

    for problem in problems:
        _ = evaluateDynamic(problem, 10)
