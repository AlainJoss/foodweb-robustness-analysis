import networkx as nx
import random
import pandas as pd
from .MetricCalculator import MetricCalculator


class Graph():
    """
    DiGraph's responsibilities are mainly to compute, keep track, and report its state.
    
    It represents a directed graph constructed from a provided edge DataFrame.
    This class contains methods for loading data into the graph, manipulating it, 
    and computing various network metrics.

    Attributes:
        nx_graph (nx.DiGraph): NetworkX directed graph instance.
        metrics_calculator (MetricCalculator): Instance to calculate network metrics.
        metrics_trend (dict): Trends of metrics computed over the course of operations.

    Methods:
        load_data: Loads data from a DataFrame into the graph.
        get_nx_graph: Returns the current NetworkX graph instance.
        set_buckets: Assigns a bucket configuration for nodes.
        copy: Returns a copy of the current graph.
        size: Returns the number of nodes in the graph.
        update_metrics_evolution: Computes and updates the metric trends.
        _compute_metrics: Computes the graph's metrics using the metrics_calculator.
        _choose_bucket: Randomly chooses a bucket based on assigned probabilities.
        choose_node: Randomly chooses a node based on bucket configurations.
        remove_node_and_dependents: Removes a node and any consequent nodes that become isolated.

    Note:
        This class assumes that the edge DataFrame provided during initialization 
        contains columns that represent source and target nodes.
    """

    def __init__(self, edge_df: pd.DataFrame, source_col: str, target_col: str) -> None:
        self.nx_graph = self.load_data(edge_df, source_col, target_col)
        self.metric_calculator = MetricCalculator()
        self.metrics_evolution = {metric: [] for metric in MetricCalculator.get_metric_names()}


    # TODO: reverse dataset instead of graph
    def load_data(self, edge_df: pd.DataFrame, source_col: str, target_col: str) -> nx.DiGraph:
        g = nx.from_pandas_edgelist(edge_df, source=source_col, target=target_col, edge_attr=True, create_using=nx.DiGraph())
        return nx.reverse(g)
    
        
    def get_nx_graph(self) -> nx.DiGraph:
        return self.nx_graph
    

    def get_metric_evolution(self) -> dict:
        return self.metrics_evolution
    

    def set_buckets(self, buckets: dict) -> None:
        self.buckets = buckets
    
    
    def size(self) -> int:
        return len(self.nx_graph)
    
    
    def update_metrics_evolution(self) -> None:
        computed_metrics = self._compute_metrics()
        for metric in self.metrics_evolution:
            self.metrics_evolution[metric].append(computed_metrics[metric])
    

    def _compute_metrics(self) -> dict:
        return self.metric_calculator.compute_metrics(self.nx_graph)


    def choose_node(self) -> str:
        chosen_bucket = self._choose_bucket()
        eligible_nodes = [node for node, data in self.nx_graph.nodes(data=True) if data['bucket'] == chosen_bucket]
        return random.choice(eligible_nodes)
    
    
    def _choose_bucket(self) -> str:
        buckets = list(self.buckets.keys())
        probabilities = list(self.buckets.values())
        return random.choices(buckets, weights=probabilities)[0]


    def remove_node_and_dependents(self, node: str) -> None:
        k_level_neighbors = set(self.nx_graph.successors(node))
        self.nx_graph.remove_node(node)

        # Explore neighbors level after level
        while len(k_level_neighbors) > 0:

            new_level_neighbors = set()
            removed_neighbors = set()

            # In the worst case the check must be done |k_level_neighbors| times
            for i in range(len(k_level_neighbors)):
                change_flag = False  # flag indicating if any nodes were removed in this loop

                for neighbor in set(k_level_neighbors):  # TODO: check scenario of copying set and without
                    
                    # A node is removed if it does not have any inward edge, if it's isolated, or if it's an isolated self-loop
                    if self.nx_graph.in_degree(neighbor) == 0 or self.nx_graph.degree(neighbor) == 0 or (self.nx_graph.in_degree(neighbor) == 1 and self.nx_graph.has_edge(neighbor, neighbor)):
                        new_level_neighbors.update(set(self.nx_graph.successors(neighbor)))
                        k_level_neighbors.remove(neighbor)
                        removed_neighbors.add(neighbor)
                        self.nx_graph.remove_node(neighbor)

                        change_flag = True
                
                if not change_flag:
                    break

            k_level_neighbors = new_level_neighbors - removed_neighbors