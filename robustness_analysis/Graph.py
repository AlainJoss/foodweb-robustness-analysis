import networkx as nx
import random
import pandas as pd
from .metric_calculator import MetricCalculator
import copy

class Graph():
    """
    Represents a directed graph with methods to perform various operations like 
    node removal, metric calculation, and more.
    
    Attributes:
    -----------
    nx_graph : NetworkX.DiGraph
        The underlying directed graph representation using NetworkX.
    metrics_calculator : MetricCalculator
        Utility to compute various metrics on the graph.
    metrics_trend : dict
        Stores the trends of metrics computed over operations on the graph.
    """

    def __init__(self, edge_df: pd.DataFrame, source: str, target: str) -> None:
        if edge_df is not None:
            self.nx_graph = self.load_data(edge_df, source, target)
        else:
            self.nx_graph = nx.DiGraph()  # Initialize an empty directed graph
        self.metric_calculator = MetricCalculator()
        self.metrics_evolution = {metric: [] for metric in MetricCalculator.get_metric_names()}


    # TODO: reverse dataset instead of graph
    def load_data(self, edge_df: pd.DataFrame, source: str, target: str) -> nx.DiGraph:
        g = nx.from_pandas_edgelist(edge_df, source=source, target=target, create_using=nx.DiGraph())
        return nx.reverse(g)
    

    def update_attributes(self, species_df: pd.DataFrame) -> None:
        """
        Updates node attributes based on the given species dataframe.
        
        Parameters:
        -----------
        species_df : pd.DataFrame
            Dataframe containing species and their habitats.
        """
        
        for _, row in species_df.iterrows():
            specie = row['Taxon']
            habitat_list = row['Habitat'].split(";")
            
            # TODO: remove appendice
            if specie in list(self.nx_graph.nodes).copy():
                self.nx_graph.nodes[specie]['Habitat'] = habitat_list
    
        
    def get_nx_graph(self) -> nx.DiGraph:
        return self.nx_graph
    

    def get_metric_evolution(self) -> dict:
        return self.metrics_evolution
    

    def set_buckets(self, buckets: dict) -> None:
        self.buckets = buckets
    
    
    def size(self) -> int:
        return len(self.nx_graph)
    

    def copy(self) -> object:
        return copy.deepcopy(self)


    def update_metrics_evolution(self) -> None:
        """
        Computes and updates the trends of various metrics.
        This might include metrics like average degree, graph density, etc.
        """
        computed_metrics = self._compute_metrics()
        for metric in self.metrics_evolution:
            self.metrics_evolution[metric].append(computed_metrics[metric])
    

    def _compute_metrics(self) -> dict:
        return self.metric_calculator.compute_metrics(self.nx_graph)
    
        
    def choose_node(self) -> str:
        chosen_bucket = self._choose_bucket()
        eligible_nodes = [node for node, data in self.nx_graph.nodes(data=True) if data.get('Bucket') == chosen_bucket]
        
        if not eligible_nodes:
            print(f"No nodes found for bucket {chosen_bucket}. Removing bucket.")
            del self.buckets[chosen_bucket]  # Remove the bucket from the dictionary
            
            # Normalize the remaining probabilities
            total_probability = sum(self.buckets.values())
            for key in self.buckets:
                self.buckets[key] /= total_probability

            return self.choose_node()  # Recursively choose another node
        return random.choice(eligible_nodes)

    
    def _choose_bucket(self) -> str:
        buckets = list(self.buckets.keys())
        probabilities = list(self.buckets.values())
        return random.choices(buckets, weights=probabilities)[0]
                
        
    def remove_node_and_dependents(self, node: str) -> None:
        """
        Removes the specified node from the graph and also removes any dependent nodes 
        that might be affected by this removal (like isolated nodes).
        
        Parameters:
        -----------
        node : Node (or appropriate type)
            The node to be removed.
        """
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