from graph import Graph
from collections import defaultdict


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
        self.save_nodes = save_nodes  # feature that track nodes in single perturbations, not meant for simulations!
        self.metric_evolution = {}


    def run(self) -> None:
        """
        Executes the perturbation on the graph. At each step, metrics are updated, 
        a node is chosen and removed, and any nodes which do not receive energy anymore are also removed.
        If the save_nodes flag is activated, the final dictionary will also track the primary extinctions. 
        """
        print("Id:", self.id, "starting simulation ...")
        while self.graph.size() > 0:
            computed_metrics = self.graph.compute_metrics()
            node = self.graph.choose_node()
            if self.save_nodes:
                computed_metrics["chosen_node"] = node
            self._update_metric_evolution(computed_metrics)
            self.graph.remove_node_and_dependents(node)

            if self.graph.size() % 1000 == 0:
                print("Id:", self.id, "Size:", self.graph.size())


    def _update_metric_evolution(self, computed_metrics: dict) -> None:
        for key, value in computed_metrics.items():
            self.metric_evolution.setdefault(key, []).append(value)
    

    def get_metric_evolution(self) -> dict:
        expanded_metrics = self._expand_list_based_on_graph_size(self.metric_evolution)
        return expanded_metrics


    def _expand_list_based_on_graph_size(self, metric_evolution: dict) -> dict:
        graph_size_list = metric_evolution['graph_size']
        expanded_dict = defaultdict(list)
        
        for i in range(len(graph_size_list) - 1):
            diff = graph_size_list[i] - graph_size_list[i+1] - 1
            for key, value_list in metric_evolution.items():
                for _ in range(diff + 1):  # +1 to include the current time step as well
                    expanded_dict[key].append(value_list[i])

        # Add the last values since they don't have a "next" value for comparison
        for key, value_list in metric_evolution.items():
            expanded_dict[key].append(value_list[-1])

        return expanded_dict

