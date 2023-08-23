from .graph import Graph
import random


class Perturbation():
    """
    Represents a perturbation process on a graph. Nodes are removed from the graph 
    until it's empty, and metrics are updated at each step.
    
    Attributes:
    -----------
    graph : AbstractGraph
        The graph on which perturbations will be performed.
    """

    def __init__(self, graph: Graph, save_nodes: bool = False) -> None:
        self.graph = graph
        # TODO: choose where to implement
        self.save_nodes = save_nodes
        self.id = str(round(random.random(), 4))


    def run(self) -> None:
        """
        Executes the perturbation on the graph. At each step, metrics are updated, 
        a node is chosen and removed, and any nodes which do not receive energy anymore are also removed.
        """
        while self.graph.size() > 0:
            if self.graph.size() % 1000 == 0:
                print("Id:", self.id, ", Size:", self.graph.size())
            self.graph.update_metrics_evolution()
            node = self.graph.choose_node()
            self.graph.remove_node_and_dependents(node)


    def get_metric_evolution(self) -> dict:
        return self.graph.get_metric_evolution()
