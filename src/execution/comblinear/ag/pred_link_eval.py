import sframe

class Hop:
    metrics = None
    results = None
    top = None
    name_of_metrics = None
    
    
    @classmethod
    def open_files(cls, arquivo1, arquivo2, top, name_of_metrics):
        cls.metrics = sframe.SFrame.read_csv(arquivo1)
        cls.results = sframe.SFrame.read_csv(arquivo2)
        cls.metrics = cls.metrics.join(cls.results)
        cls.top = top
        cls.name_of_metrics = name_of_metrics

    def __init__(self):
        pass

    @classmethod
    def evaluate(cls, individual):
        new_metric = 0
        for index in range(len(cls.name_of_metrics)):
            new_metric = new_metric + (cls.metrics[cls.name_of_metrics[index]] * individual[index]) 
        
        cls.metrics.add_column(new_metric, name='new_metric')
        top_metrics = cls.metrics.topk('new_metric', k=cls.top)
        aux = [0]
        top_metrics = top_metrics.filter_by(aux,'result')
        zero = top_metrics.num_rows()
        cls.metrics.remove_column('new_metric')
        return 1 - float(zero) / cls.top,

