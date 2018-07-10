# Markov Chain Monte Carlo - 0/1 Knapsack Problem

This repository refers to the final work of the discipline: **Special Topics in Monte Carlo Algorithms and Markov Chains**, PESC / COPPE / UFRJ [CPS767](http://land.ufrj.br/~daniel/mcmc/), taught by Professor [Daniel R. Figueiredo](http://www.land.ufrj.br/~daniel/) during the first semester of 2018.

**Students:**

* [Marcos Aurélio C de S Filho](https://github.com/Maasouza)
* [Rafael G Damasceno](https://github.com/DamascenoRafael)


## About

The objective of this repository is to establish solutions for the 0/1 Knapsack Problem, that is, each element may or may not be in the solution without repetition. The developed code aims to evaluate the results and performance of different algorithms involving Markov Chains Monte Carlo. The techniques covered involved the algorithms of Random Walk, Metropolis Hastings, Simulated Annealing in different cooling and transition strategies in contrast to the pseudo-polynomial solution algorithm and also the greedy algorithm known as Hill Climbing. In addition, this repository seeks to raise the possible scenarios in which Markov Chain Monte Carlo have an advantage over the deterministic algorithms.

## Running algorithms

All algorithms are written using [Python 3](https://www.python.org/) and are available in the `src` directory. In the `data` directory you can find some problems that can be executed by the algorithms.

The different algorithms involving Markov Chains Monte Carlo can be run through the file `src/main.py`, where there are comments explaining how to select the problems, the algorithms and the ways of performance evaluation.

The greedy solution can be executed through the `src/dynamic-solution.py` file where the problems to be executed can be selected. This solution is feasible only for small instances.

