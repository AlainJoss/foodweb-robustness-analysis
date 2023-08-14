import networkx as nx
import pandas as pd

class DiGraph():
    def __init__(self, edge_df: pd.DataFrame, source_col: str = 'Source_Name', target_col: str = 'Target_Name') -> None:
        self.graph = self.load_data(edge_df, source_col, target_col)

    def load_data(self, edge_df: pd.DataFrame, source_col: str, target_col: str) -> nx.DiGraph:
        return nx.from_pandas_edgelist(edge_df, source=source_col, target=target_col, edge_attr=True, create_using=nx.DiGraph())
    
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
