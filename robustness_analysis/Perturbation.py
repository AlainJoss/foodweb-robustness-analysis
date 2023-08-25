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

    def __init__(self, id, graph: Graph, save_nodes: bool) -> None:
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
        self.id = "{:04}".format(id)
        self.graph = graph
        self.metric_evolution = {}
        self.save_nodes = save_nodes
        self.node_evolution = {'removal_type': [], 'node': []}

    def run(self) -> None:
        """
        Executes the perturbation process on the graph. At each step:
        1. Metrics are computed and updated.
        2. A node is selected for removal.
        3. The chosen node and any dependent nodes are removed from the graph.
        
        If the `save_nodes` flag is enabled, the nodes removed during each perturbation step are recorded.
        Progress updates are printed for every 1000 nodes removed.
        """
        print(">>> perturbation", self.id, "started")
        while self.graph.size() > 0:
            computed_metrics = self.graph.compute_metrics()
            node = self.graph.choose_node()
            self._update_metric_evolution(computed_metrics)
            dependents = self.graph.remove_node_and_dependents(node)

            if self.save_nodes:
                self.node_evolution['removal_type'].append("primary")
                self.node_evolution['node'].append(node)
                if len(dependents) > 0:
                    self.node_evolution['removal_type'].extend(["secondary"] * len(dependents))
                    self.node_evolution['node'].extend(dependent_node for dependent_node in dependents)

            if self.graph.size() % 1000 == 0:
                print("id:", self.id, "-> size:", self.graph.size())


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
        if self.save_nodes:
            expanded_metrics['node'] = self.node_evolution['node']
            expanded_metrics['removal_type'] = self.node_evolution['removal_type']
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

        Example:
        --------
        index: [0, 1, 2, ...]
        {
            'graph_size' = [100, 97, 96, ...]
            'avg_degree' = [7, 3, 5, ...]
        }

        after _expand_list_based_on_graph_size:

        index: [0, 1, 2, 3, 4, ...]
        {
            'graph_size' = [100, 100, 100, 97, 96, ...]
            'avg_degree' = [7, 7, 7, 3, 5, ...]
        }
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
