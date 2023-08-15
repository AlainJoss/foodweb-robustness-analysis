from .DiGraph import DiGraph
from .AttackStrategy import AttackStrategy


class Perturbation():

    def __init__(self, graph: DiGraph, strategy: AttackStrategy) -> None:
        self.graph = graph
        self.strategy = strategy
        created_buckets = self._create_buckets()
        self.graph.set_buckets(created_buckets)


    def _create_buckets(self) -> dict:
        nx_graph = self.graph.get_nx_graph()
        return self.strategy.create_buckets(nx_graph)
    

    def run(self) -> None:
        while self.graph.size() > 0:
            print(self.graph.size())
            self.graph.update_metrics()
            node = self.graph.choose_node()
            self.graph.remove_node_and_consequent(node)


    def get_results(self) -> dict:
        return self.graph.metric_trend
