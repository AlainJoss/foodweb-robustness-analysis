import networkx as nx
import random
import pandas as pd
import numpy as np

class DiGraph():
    def __init__(self, edge_df: pd.DataFrame, source_col: str = 'Source_Name', target_col: str = 'Target_Name') -> None:
        self.graph = self.load_data(edge_df, source_col, target_col)
        self.metrics = [self.average_in_degree, self.density]

    # TODO: reverse dataset instead of graph
    def load_data(self, edge_df: pd.DataFrame, source_col: str, target_col: str) -> nx.DiGraph:
        g = nx.from_pandas_edgelist(edge_df, source=source_col, target=target_col, edge_attr=True, create_using=nx.DiGraph())
        return nx.reverse(g)
    

    def copy(self) -> object:
        return self.graph.copy()
    
    def size(self) -> int:
        return self.graph.number_of_nodes()
    
    
    def compute_metrics(self) -> dict:
        return {metric.__name__: metric() for metric in self.metrics}


    def average_in_degree(self) -> float:
        n = self.size()
        total_in_degree = sum(dict(self.graph.in_degree()).values())
        avg_in_degree = total_in_degree / n
        return avg_in_degree

    
    def density(self) -> float:
        n = self.size() 
        if n < 2:
            return 0  # or some other value to indicate the graph is too small
        return nx.density(self.graph)

    
    
    # TODO: implement other metrics
    

    def create_random_buckets(self) -> dict:
        for node in self.graph.nodes():
            self.graph.nodes[node]['bucket'] = 'b1'
        self.buckets = {'b1': 1.0}
    

    def create_sequential_buckets(self) -> dict:
        self.buckets = None


    def create_threatened_habitats_buckets(self, threatened_habitats: list =[]) -> dict:
        # TODO: collect information from attributes of nodes
        self.buckets = None


    def create_threatened_species_buckets(self, threatened_species: list = []) -> dict:
        # TODO: collect information from attributes of nodes
        self.buckets = None
    

    def _choose_bucket(self) -> str:
        buckets = list(self.buckets.keys())
        probabilities = list(self.buckets.values())
        return random.choices(buckets, weights=probabilities)[0]


    def choose_node(self) -> str:
        chosen_bucket = self._choose_bucket()
        eligible_nodes = [node for node, data in self.graph.nodes(data=True) if data['bucket'] == chosen_bucket]
        return random.choice(eligible_nodes)


    def node_removal(self, node: str) -> None:
        k_level_neighbors = set(self.graph.successors(node))
        self.graph.remove_node(node)

        # Explore neighbors level after level
        while len(k_level_neighbors) > 0:

            new_level_neighbors = set()
            removed_neighbors = set()

            # In the worst case the check must be done |k_level_neighbors| times
            for i in range(len(k_level_neighbors)):
                change_flag = False  # flag indicating if any nodes were removed in this loop

                for neighbor in set(k_level_neighbors):  # TODO: check scenario of copying set and without
                    
                    # A node is removed if it does not have any inward edge, if it's isolated, or if it's an isolated self-loop
                    if self.graph.in_degree(neighbor) == 0 or self.graph.degree(neighbor) == 0 or (self.graph.in_degree(neighbor) == 1 and self.graph.has_edge(neighbor, neighbor)):
                        new_level_neighbors.update(set(self.graph.successors(neighbor)))
                        k_level_neighbors.remove(neighbor)
                        removed_neighbors.add(neighbor)
                        self.graph.remove_node(neighbor)

                        change_flag = True
                
                if not change_flag:
                    break

            k_level_neighbors = new_level_neighbors - removed_neighbors


    def in_degree_centrality(self) -> dict:
        return nx.in_degree_centrality(self.graph)

    # TODO: implement other metrics