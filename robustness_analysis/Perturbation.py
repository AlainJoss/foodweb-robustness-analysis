from DiGraph import DiGraph
from AttackStrategy import AttackStrategy
from MetricCalculator import MetricCalculator

class Perturbation():

    def __init__(self, graph: DiGraph, strategy: AttackStrategy) -> None:
        self.graph = graph
        self.strategy = strategy
        self.buckets = self._create_buckets()
        self.metric_trend = {metric: [] for metric in MetricCalculator.get_metric_names()}


    def _create_buckets(self) -> dict:
        return self.strategy.create_buckets(self.graph.graph)


    def run(self) -> None:
        while self.graph.size() > 0:
            computed_metrics = self.graph.compute_metrics()
            for metric in self.metric_trend:
                self.metric_trend[metric].append(computed_metrics[metric])
            
            node = self.graph.choose_node()
            self.graph.remove_node_and_consequent(node)
            

    def get_results(self) -> dict:
        return self.metric_trend