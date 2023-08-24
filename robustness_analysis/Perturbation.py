from graph import Graph


class Perturbation():
    """
    Represents a perturbation process on a graph. Nodes are removed from the graph 
    until it's empty, and metrics are updated at each step.
    
    Attributes:
    -----------
    graph : AbstractGraph
        The graph on which perturbations will be performed.
    """

    def __init__(self, id, graph: Graph, save_nodes: bool = False) -> None:
        self.id = id
        self.graph = graph
        # TODO: choose where to implement
        self.save_nodes = save_nodes
        self.metric_evolution = {}


    def run(self) -> None:
        """
        Executes the perturbation on the graph. At each step, metrics are updated, 
        a node is chosen and removed, and any nodes which do not receive energy anymore are also removed.
        """
        print("Id:", self.id, "starting simulation ...")
        while self.graph.size() > 0:
            computed_metrics = self.graph.compute_metrics()
            self._update_metric_evolution(computed_metrics)
            node = self.graph.choose_node()
            self.graph.remove_node_and_dependents(node)

            if self.graph.size() % 1000 == 0:
                print("Id:", self.id, "Size:", self.graph.size())


    def _update_metric_evolution(self, computed_metrics: dict) -> None:
        for key, value in computed_metrics.items():
            self.metric_evolution.setdefault(key, []).append(value)
    

    def get_metric_evolution(self) -> dict:
        return self.metric_evolution
