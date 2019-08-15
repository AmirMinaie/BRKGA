import TSCFLP
import BRKGA
import random
import time
import LocalSearch

# Number of plants
I = 16
# Number of depots
J = 16
# Number of customer
K = 14
# fi is the fixed cost associated to plant i ∈ I
f = [random.uniform(2 * 10 ^ 4, 3 * 10 ^ 4) for i in range(I)]
# gj is the fixed cost associated to depot j ∈ J;
g = [random.uniform(8 * 10 ^ 3, 12 * 10 ^ 3) for i in range(I)]
# cij is the transportation cost of one unit of the product between plant i ∈ I and depot j ∈ J;
c = [[random.uniform(35, 45) for J in range(J)] for i in range(I)]
# djk is the transportation cost of one unit of the product between depot j ∈ J and customer k ∈ K ;
d = [[random.uniform(55, 65) for k in range(K)] for j in range(J)]
# qk is the demand of customer k ∈ K;
q = [random.uniform(10, 20) for k in range(K)]
# bi is the capacity of plant i ∈ I
b = [random.uniform(2 * 10 ^ 6, 5 * 10 ^ 6) for i in range(I)]
# pj is the capacity of satellite j ∈ J.
pj = [random.uniform(2 * 10 ^ 6, 5 * 10 ^ 6) for j in range(J)]

# number of genes in a chromosome
n = I + J + K
# population size
p = 4 * n
# size of elite solution population
pe = int(0.13 * p)
# size of the mutant solution population
pm = int(0.17 * p)
# probability that the gene of the offspring inherits the allele of the elite parent.
poe = 0.69

# Number of LocalSearch
LS = 10

t = TSCFLP.TSCFLP(I, J, K, f, g, c, d, q, b, pj)

b = BRKGA.BRKGA(n, p, pe, pm, poe, t.Z)

tic = time.process_time()

print("Genetic Algorithm")
print("#    Fitness")

P = b.GA()

print("Local Search")
print("#    Fitness")

PL = LocalSearch.LocalSearch(p[0][0:10])

toc = time.process_time()

print("\n\nTimer = " + str(toc - tic))
print("F(y,z,x,s) = " + str(p[0][0].fitnes))
print("Y = " + str(p[0][0].y))
print("Z = " + str(p[0][0].z))
print("X = " + str(p[0][0].x))
print("S = " + str(p[0][0].s))
