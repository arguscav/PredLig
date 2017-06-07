# coding=UTF-8

'''
Created on 6 de jul de 2016

@author: Administrador
'''

import random

from deap import base
from deap import creator
from deap import tools
import pred_link_eval
from scoop import futures
from pickle import POP


IND_SIZE = 7


def my_random():
    return random.uniform(-1, 1)


def eval(individual):
    return pred_link_eval.Hop.evaluate(individual)
    
def cross(individual1, individual2):
    a = random.random()
    ind1 = []
    ind2 = []
    for i in range(len(individual1)):
        ind1.append(a * individual1[i] + (1 - a) * individual2[i])
        ind2.append((1 - a) * individual1[i] + a * individual2[i])
    return individual1, individual2



class GA(object):
    def __init__(self, quantity_of_metrics, metricas, resultados, top, name_of_metrics, melhoresMetricas):
        self.quantity_of_metrics = quantity_of_metrics
        self.metrica_path = metricas
        self.name_of_metrics = name_of_metrics;
        pred_link_eval.Hop.open_files(metricas, resultados, top, name_of_metrics )
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", my_random)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                        self.toolbox.attr_float, n=self.quantity_of_metrics)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", eval,  )
        self.toolbox.register("mutate", tools.mutGaussian, indpb=0.05, mu=0, sigma=2.0)
        self.toolbox.register("mate", cross)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
    
    def inicializarPopulacao(self, melhoresMetricas):
        
        #Convertendo a lista de métricas em uma lista de índices 
        melhoresMetricasPorIndice = []
        for metrica in melhoresMetricas:
            melhoresMetricasPorIndice.append(self.name_of_metrics.index(metrica))  
         
        solucoesInicializadas = 0
        #Sementes iniciais - melhores resultados individuais
        pop = self.toolbox.population(n=100)
        for j in range(self.quantity_of_metrics):
            for i in range(self.quantity_of_metrics):
                if i != j:
                    pop[j][i] = 0
                else:
                    pop[j][i] = 1
            solucoesInicializadas += 1
        
        #Combinações 2 a 2 das 3 metricas com melhor desempenho individual
        for i in range(len(melhoresMetricasPorIndice) - 1):
            for j in range(i+1, len(melhoresMetricasPorIndice)):
                parDeMelhoresMetricas = [melhoresMetricasPorIndice[i], melhoresMetricasPorIndice[j]] 
                for k in range(self.quantity_of_metrics):
                    if k in parDeMelhoresMetricas:
                        pop[solucoesInicializadas][k] = 1
                    else:
                        pop[solucoesInicializadas][k] = 0
                solucoesInicializadas += 1    
        
        #Inicializando uma solucao com as 3 melhores métricas
        for i in range(self.quantity_of_metrics):
            if i in melhoresMetricasPorIndice:
                pop[solucoesInicializadas][i] = 1
            else:
                pop[solucoesInicializadas][i] = 0
        solucoesInicializadas += 1    
        
        return pop
    
    def execucao(self):
        arquivo_de_resultados = open( self.metrica_path + '.pesos.txt', 'a')

        random.seed(128)

        pop = self.inicializarPopulacao(melhoresMetricas) 
        
        CXPB, MUTPB, NGEN = 0.65, 0.08, 100
        
        print("Start of evolution")
        # Evaluate the entire population
        fitnesses = list(map(self.toolbox.evaluate, pop ))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(pop))

        for g in range(NGEN):
            print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)

                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                # mutate an individual with probability MUTPB
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            print("  Evaluated %i individuals" % len(invalid_ind))

            # The population is entirely replaced by the offspring
            
            pop[0] = tools.selBest(pop, 1)[0]
            pop[1:] = offspring[1:]

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]


            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5

            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)

        print("-- End of (successful) evolution --")

        best_ind = tools.selBest(pop, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
        arquivo_de_resultados.write("******Execucao*********\nBest individual is: " + ' '.join(map(str, best_ind)) + "\nFitness value: " + str(best_ind.fitness.values[0]) + "\n")
            


if __name__ == "__main__":
    #gr-qc
    metricas = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/grqc_1994_1999/CombinationLinear/ToAG/data.csv'
    resultados = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/grqc_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes.csv'

    melhoresMetricas = ['cn', 'ts05', 'ts02']
    ag = GA(7, metricas, resultados, 205, ['cn', 'aas', 'pa', 'jc', 'ts08', 'ts05', 'ts02'], melhoresMetricas)
    ag.execucao()

    #hep-th
    metricas = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/hepth_1994_1999/CombinationLinear/ToAG/data.csv'
    resultados = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/hepth_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes.csv'
    
    melhoresMetricas = ['jc', 'cn', 'ts05']
    ag = GA(7, metricas, resultados, 930, ['cn', 'aas', 'pa', 'jc', 'ts08', 'ts05', 'ts02'], melhoresMetricas)
    ag.execucao()

    #hep-ph
    metricas = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/hepph_1994_1999/CombinationLinear/ToAG/data.csv'
    resultados = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/hepph_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes.csv'

    melhoresMetricas = ['aas', 'jc', 'ts02']
    ag = GA(7, metricas, resultados, 4848, ['cn', 'aas', 'pa', 'jc', 'ts08', 'ts05', 'ts02'], melhoresMetricas)
    ag.execucao()

    #cond-mat
    metricas = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/condmat_1994_1999/CombinationLinear/ToAG/data.csv'
    resultados = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/condmat_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes.csv'

    melhoresMetricas = ['ts02', 'ts05', 'jc']
    ag = GA(7, metricas, resultados, 651, ['cn', 'aas', 'pa', 'jc', 'ts08', 'ts05', 'ts02'], melhoresMetricas)
    ag.execucao()

    #astro-ph
    metricas = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/astroph_1994_1999/CombinationLinear/ToAG/data.csv'
    resultados = '/Mestrado-2016/git/Predicao-de-Links/PredLig/src/formating/results/grafos_nowell/astroph_1994_1999/CombinationLinear/ToAG/analysed.txt.allNodes.csv'

    melhoresMetricas = ['aas', 'cn', 'ts02']
    ag = GA(7, metricas, resultados, 1975, ['cn', 'aas', 'pa', 'jc', 'ts08', 'ts05', 'ts02'], melhoresMetricas)
    ag.execucao()
    
    
