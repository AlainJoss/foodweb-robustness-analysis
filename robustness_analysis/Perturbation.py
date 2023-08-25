from graph import Graph
from collections import defaultdict

class Perturbation():
    """
    Represents a perturbation process on a graph. Nodes are removed from the graph 
    until it's empty, and metrics are updated at each step.
    
    Attributes:
    -----------
    graph : Graph
        The graph on which perturbations will be performed.
    """

    def __init__(self, id, graph: Graph, save_nodes: bool = False) -> None:
        """
        Initializes the Perturbation with a graph and optional settings.
        
        Parameters:
        -----------
        id : int
            Identifier for the perturbation.
        graph : Graph
            The graph on which perturbations will be performed.
        save_nodes : bool, optional
            Flag to track nodes during perturbations. Not intended for simulations. Default is False.
        """
        self.id = id
        self.graph = graph
        self.save_nodes = save_nodes
        self.metric_evolution = {}


    def run(self) -> None:
        """
        Executes the perturbation process on the graph. Metrics are updated at each step, 
        nodes are chosen and removed, and any dependent nodes are also removed.
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
        """
        Updates the metric evolution dictionary with the computed metrics.
        
        Parameters:
        -----------
        computed_metrics : dict
            The metrics computed at the current step.
        """
        for key, value in computed_metrics.items():
            self.metric_evolution.setdefault(key, []).append(value)


    def get_metric_evolution(self) -> dict:
        """
        Returns the expanded metric evolution based on graph size.
        
        Returns:
        --------
        dict
            The expanded metric evolution.
        """
        expanded_metrics = self._expand_list_based_on_graph_size(self.metric_evolution)
        return expanded_metrics


    def _expand_list_based_on_graph_size(self, metric_evolution: dict) -> dict:
        """
        Expands the metric evolution list based on the graph size. This is useful 
        for visualizing the evolution over consistent time steps.
        
        Parameters:
        -----------
        metric_evolution : dict
            The original metric evolution dictionary.
        
        Returns:
        --------
        dict
            The expanded metric evolution.
        """
        graph_size_list = metric_evolution['graph_size']
        expanded_dict = defaultdict(list)
        
        for i in range(len(graph_size_list) - 1):
            diff = graph_size_list[i] - graph_size_list[i+1] - 1
            for key, value_list in metric_evolution.items():
                for _ in range(diff + 1):
                    expanded_dict[key].append(value_list[i])

        for key, value_list in metric_evolution.items():
            expanded_dict[key].append(value_list[-1])

        return expanded_dict
