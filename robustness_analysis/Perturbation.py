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

    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        self.id = str(round(random.random(), 4))


    def run(self) -> None:
        """
        Executes the perturbation on the graph. At each step, metrics are updated, 
        a node is chosen and removed, and any nodes which do not receive energy anymore are also removed.
        """
        while self.graph.size() > 0:
            if self.graph.size() % 100 == 0:
                print("Id:", self.id, ", Size:", self.graph.size())
                print(self.graph.get_metric_evolution()['number_of_wccs'][-1])
            self.graph.update_metrics_evolution()
            node = self.graph.choose_node()
            self.graph.remove_node_and_dependents(node)


    def get_metric_evolution(self) -> dict:
        return self.graph.get_metric_evolution()
