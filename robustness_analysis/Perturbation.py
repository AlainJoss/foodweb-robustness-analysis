from .Graph import Graph
from .AttackStrategy import AttackStrategy


class Perturbation():
    """
    Perturbation's responisibilities are mainly to tell the AttackStrategy to create buckets,
    and to manipulate the graph in the perturbation process.
    
    The perturbation is performed by selecting and removing nodes from the graph 
    according to the designated strategy until no nodes remain. 
    At the end, the results stored in graph are retrieved for passing them to Simulation.
    
    Attributes:
        graph (DiGraph): The directed graph to be perturbed.
        strategy (AttackStrategy): The strategy used to select nodes for removal.
    
    Methods:
        run: Executes the perturbation process until the graph is empty. 
             During each iteration, the graph metrics are updated, a node is selected based on the strategy, 
             and the node along with its dependents are removed from the graph.
             
        get_results: Returns the evolution of metrics throughout the perturbation process.
    """

    def __init__(self, graph: Graph, strategy: AttackStrategy) -> None:
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
            self.graph.update_metrics_evolution()
            node = self.graph.choose_node()
            self.graph.remove_node_and_dependents(node)


    def get_metric_evolution(self) -> dict:
        return self.graph.get_metric_evolution()
