import random
import math


class BRKGA:
    # number of genes in a chromosome
    n = None
    # population size
    p = None
    # size of elite solution population
    pe = None
    # size of the mutant solution population
    pm = None
    # probability that the gene of the offspring inherits the allele of the elite parent.
    poe = None
    # Fitness
    Fitness = None

    def __init__(self, n, p, pe, pm, poe, Fitness):
        self.n = n
        self.p = p
        self.pe = pe
        self.pm = pm
        self.poe = poe
        self.Fitness = Fitness

    def GA(self):

        population = self.GenerateIntipopulation()
        RecordIteration = []

        for chrom in population:
            chrom = self.Fitness(chrom)

        # Sort solutions by their costs
        population = sorted(population, key=lambda x: x.fitnes, reverse=False)
        RecordIteration.append(population[0])

        a = True
        while a:

            print(str(len(RecordIteration)) + "  " + str(population[0].fitnes))

            # Classify solutions as elite or non-elite
            elitePopulation = population[0: self.pe]
            nonElitePopulation = population[self.pe:len(population)]

            # Copy elite solutions to next population
            newPopulation = []
            newPopulation.extend(elitePopulation)

            # Generate mutants in next population
            newPopulation.extend([self.GenerateChromosome() for i in range(self.pm)])

            # Combine elite and non-elite solutions and add children to next population
            for i in range(self.p - self.pe - self.pm):
                eliteParent = random.choice(elitePopulation)
                nonEliteParent = random.choice(nonElitePopulation)
                genes = []
                for i in range(self.n):
                    r = random.random()
                    if r < self.poe:
                        genes.append(eliteParent.genes[i])
                    else:
                        genes.append(nonEliteParent.genes[i])
                newPopulation.append(chromosome(genes))

            for chrom in newPopulation:
                if chrom.fitnes == None:
                    chrom = self.Fitness(chrom)

            population = newPopulation

            # Sort solutions by their costs
            population = sorted(population, key=lambda x: x.fitnes, reverse=False)
            RecordIteration.append(population[0])

            if len(RecordIteration) > 31:
                a = sum(re.fitnes for re in RecordIteration[-30:]) / 30 - population[0].fitnes > 0.01

        return [population, RecordIteration]

    # Generate P vectors of random keys
    def GenerateIntipopulation(self):
        population = []
        for i in range(0, self.p):
            population.append(self.GenerateChromosome())
        return population

    def GenerateChromosome(self):
        genes = []
        for i in range(0, self.n):
            genes.append(self.GenreateGene())
        return chromosome(genes)

    def GenreateGene(self):
        return random.random()


class chromosome:
    genes = []
    y = []
    z = []
    x = []
    s = []
    fitnes = None

    def __init__(self, genes):
        self.genes = genes
