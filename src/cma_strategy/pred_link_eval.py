import sframe
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from formating.FormatingDataSets import FormatingDataSets
import numpy



class SFrame:
    
    #util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999/AllExecutionScores/configToAG.txt')
    util = ParameterUtil(parameter_file = 'data/configuration/arxiv/exemplo_1994_1999/CombinationLinear/configToAG.txt')
    #util = ParameterUtil(parameter_file = 'data/configuration/arxiv/condmat_1994_1999/CombinationLinear/configToAG.txt')
    
    
    myparams = Parameterization(t0 = util.t0, t0_ = util.t0_, t1 = util.t1, t1_ = util.t1_, linear_combination=util.linear_combination,
                                filePathGraph = util.graph_file, filePathTrainingGraph = util.trainnig_graph_file, filePathTestGraph = util.test_graph_file, decay = util.decay, domain_decay = util.domain_decay, min_edges = util.min_edges, scoreChoiced = util.ScoresChoiced, weightsChoiced = util.WeightsChoiced, weightedScoresChoiced = util.WeightedScoresChoiced, FullGraph = None, result_random_file=util.result_random_file)
     
    metrics = sframe.SFrame.read_csv(FormatingDataSets.get_abs_file_path(util.calculated_file+'_normalizated.csv'))
    results = sframe.SFrame.read_csv(FormatingDataSets.get_abs_file_path(util.result_random_file))

    top = 20
    
    def __init__(self):
        pass
        

    @classmethod
    def evaluate(cls, individual):
        new_metric = float(0)
        ##print 'individuos: ', individual
        
        for index_score in  range(len(cls.myparams.ScoresChoiced)):
            #print cls.myparams.ScoresChoiced[index_score][0].getName()
            valorMetrica = cls.metrics[ cls.myparams.ScoresChoiced[index_score][0].getName() ]
            valorIndividual = individual[index_score]
            #print "valores ", valorMetrica, valorIndividual
            new_metric = new_metric + (valorMetrica * valorIndividual )
               
        ##print 'nova metrica',  new_metric
        copy_metrics = cls.metrics.copy()
        copy_metrics.add_column(new_metric, name='new_metric')
        copy_metrics = copy_metrics.topk('new_metric', k=cls.top)
        #print 'metrics after topk \n\n', copy_metrics
        copy_results = cls.results.copy()
        
        #print 'copy_results before join', copy_results
        copy_metrics = copy_metrics.join(copy_results)
        #print 'metrics after join \n\n', copy_metrics
        copy_metrics = copy_metrics.sort('new_metric', ascending=False)
        ##print 'copy metrics ', copy_metrics
        aux = [0]
        
        copy_metrics = copy_metrics.filter_by(aux,'result')
        zero = copy_metrics.num_rows()
        #print 'zero', zero
        del copy_metrics
        del copy_results
        result =  float(zero) / cls.top,
        #print 'resultado ', result
        return result