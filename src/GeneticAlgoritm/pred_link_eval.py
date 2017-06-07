import sframe
from parametering.ParameterUtil import ParameterUtil
from parametering.Parameterization import Parameterization
from formating.FormatingDataSets import FormatingDataSets



class SFrame:
    
    util = ParameterUtil(parameter_file = 'data/formatado/arxiv/nowell_astroph_1994_1999/AllExecutionScores/configToAG.txt')
    
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
        
        for index_score in  range(len(cls.myparams.ScoresChoiced)):
            new_metric = new_metric + (cls.metrics[ cls.myparams.ScoresChoiced[index_score][0].getName() ] * individual[index_score] )
               
        print new_metric
        copy_metrics = cls.metrics.copy()
        copy_metrics.add_column(new_metric, name='new_metric')
        copy_metrics = copy_metrics.topk('new_metric', k=cls.top)
        copy_results = cls.results.copy()
        copy_metrics = copy_metrics.join(copy_results)
        copy_metrics = copy_metrics.sort('new_metric', ascending=False)
        aux = [0]
        copy_metrics = copy_metrics.filter_by(aux,'result')
        zero = copy_metrics.num_rows()
        del copy_metrics
        del copy_results
        return float(zero) / cls.top,
