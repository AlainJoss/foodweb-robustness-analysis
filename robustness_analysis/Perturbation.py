from .Graph import Graph
from .AttackStrategy import AttackStrategy


class Perturbation():
    """
    Represents a perturbation process on a graph. Nodes are removed from the graph 
    until it's empty, and metrics are updated at each step.
    
    Attributes:
    -----------
    graph : AbstractGraph
        The graph on which perturbations will be performed.
    """

    def __init__(self, graph: Graph) -> None:
        self.graph = graph


    def run(self) -> None:
        """
        Executes the perturbation on the graph. At each step, metrics are updated, 
        a node is chosen and removed, and any nodes which do not receive energy anymore are also removed.
        """
        while self.graph.size() > 0:
            print(self.graph.size())
            self.graph.update_metrics_evolution()
            node = self.graph.choose_node()
            self.graph.remove_node_and_dependents(node)


    def get_metric_evolution(self) -> dict:
        return self.graph.get_metric_evolution()
