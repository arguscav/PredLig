import numpy

from deap import algorithms
from deap import base
from deap import cma
from deap import creator
from deap import tools
import pred_link_eval
#from scoop import futures

# Problem size
#N=8
N=len(pred_link_eval.SFrame.myparams.ScoresChoiced)

# -1 means we are approaching a minimization problem
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # , must be used because deap is used for multi-obj optm
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("evaluate", pred_link_eval.SFrame.evaluate)
#toolbox.register("map", futures.map)


def main():
    
    # to generate the aleatory values we need a seed
    numpy.random.seed(128)
    file1 = open('config.txt', 'r')
    line = file1.readline()
    line = line.strip('\n').strip('\r').split(',')
    pred_link_eval.top = int(line[2])
    strategy = cma.Strategy(centroid=[5.0]*N, sigma=float(line[0]), lambda_=int(line[1]))
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    algorithms.eaGenerateUpdate(toolbox, ngen=int(line[3]), stats=stats, halloffame=hof, verbose=True)
    file1.close()
    output = open('output.txt', 'w')
    for item in hof[0]:
        output.write("%s," % item)
    output.close()
if __name__ == "__main__":
    main()