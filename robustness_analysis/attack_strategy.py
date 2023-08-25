from abc import ABC, abstractmethod
import networkx as nx
import random
import pandas as pd
from constants import ALL_SPECIES_AND_FOOD_GROUPS
from enum import Enum


class AttackStrategy(ABC):
    """
    Abstract base class for attack or perturbation strategies on a graph.
    Derived classes should define methods to categorize or select nodes in the graph 
    based on specific criteria or configurations.
    """

    @abstractmethod
    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        """
        Abstract method to setup the attack strategy for the given graph.
        
        Parameters:
        -----------
        nx_graph : nx.DiGraph
            The directed graph for which the attack strategy is to be set up.
        """
        pass

class Random(AttackStrategy):
    """
    Represents a random attack strategy on the graph.
    Nodes are chosen randomly for perturbation.
    """

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        """
        No setup required for the random strategy.
        """
        pass

    
    def choose_node(self, nx_graph: nx.DiGraph) -> str:
        """
        Chooses a node randomly from the graph.
        
        Parameters:
        -----------
        nx_graph : nx.DiGraph
            The directed graph from which a node is to be chosen.
        
        Returns:
        --------
        str
            The chosen node.
        """
        return random.choice(list(nx_graph.nodes()))
    

class Sequential(AttackStrategy):
    """
    Represents a sequential attack strategy on the graph.
    Nodes are chosen based on a specific metric, in decreasing order of their values.
    """

    class SortBy(Enum):
        """
        Enumeration for the different metrics based on which nodes can be sorted.
        """
        DEGREE = nx.degree_centrality
        IN_DEGREE = nx.in_degree_centrality
        OUT_DEGREE = nx.out_degree_centrality
        CLOSENESS = nx.closeness_centrality
        BETWEENNESS = nx.betweenness_centrality
        EDGE_BETWEENNESS = nx.edge_betweenness_centrality
        TROPHIC_LEVELS = nx.trophic_levels

    def __init__(self, metric: SortBy) -> None:
        self.metric = metric
        self.sorted_nodes = []

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> None:
        metric_values = self.metric(nx_graph)
        self.sorted_nodes = sorted(metric_values, key=metric_values.get, reverse=True)

    def choose_node(self, nx_graph: nx.DiGraph) -> str:
        return self.sorted_nodes.pop(0)
    

class ThreatenedHabitats(AttackStrategy):
    """
    Represents an attack strategy based on threatened habitats.
    Nodes (species) residing in threatened habitats are chosen based on their respective probabilities.
    """

    def __init__(self, threatened_habitats: list, min_probability: int = 0.05):
        """
        Initializes the ThreatenedHabitats attack strategy.

        Parameters:
        -----------
        threatened_habitats : list
            List of habitats that are considered threatened.
        min_probability : int, optional
            Minimum probability for a habitat to be chosen. Default is 0.05.
        """
        self.threatened_habitats = threatened_habitats
        self.min_probability = min_probability
        self.buckets = {}
        

    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> dict:

        species_df = pd.read_csv(ALL_SPECIES_AND_FOOD_GROUPS, usecols=['Taxon', 'Habitat'])
        self._set_habitats(nx_graph, species_df)

        # Step 1: Attach proportion to nodes and add to proportion to set of proportions
        proportions = set()
        for node, data in nx_graph.nodes(data=True):
            habitats = [habitat.strip() for habitat in data.get('Habitat', [])]  # Stripping whitespaces
            
            threatened_count = sum(1 for habitat in habitats if habitat in self.threatened_habitats)
            proportion = threatened_count / len(habitats) if habitats else 0.0
            nx_graph.nodes[node]["Bucket"] = str(proportion)

            proportions.add(proportion)

        # Step 2: Create buckets dictionary to return
        buckets = {}
        for prop in proportions:
            buckets[str(prop)] = prop

        # Step 3: Retrieve smallest proportion
        min_proportion = min(buckets.values())

        # Step 4: Compute x using the smallest proportion
        n = len(proportions)
        s = sum(proportions)
        x = self.min_probability*s / (1 - self.min_probability*n) - min_proportion * (1 - self.min_probability*n)

        # Step 5: Compute denominator for normalizing to probability
        proportions.discard(100) # remove fake proportion before computing
        denominator = sum(proportion + x for proportion in proportions)

        # Step 5: Update proportions
        buckets = {bucket: (prop + x) / denominator for bucket, prop in buckets.items()}

        # Step 6: Set buckets
        self.buckets = buckets


    def _set_habitats(self, nx_graph: nx.DiGraph, species_df: pd.DataFrame) -> None:

        for _, row in species_df.iterrows():
            specie = row['Taxon']
            habitat_list = row['Habitat'].split(";")
            
            if specie in list(nx_graph.nodes).copy():
                nx_graph.nodes[specie]['Habitat'] = habitat_list


    def choose_node(self, graph: nx.DiGraph) -> str:
        chosen_bucket = self._choose_bucket()
        eligible_nodes = [node for node, data in graph.nodes(data=True) if data.get('Bucket') == chosen_bucket]
        
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


class ThreatenedSpecies(AttackStrategy):

    def __init__(self, threatened_species: list = None):
        self.threatened_species = threatened_species


    def setup_attack_strategy(self, nx_graph: nx.DiGraph) -> dict:
        """
        1. Assign to each node the category according to the information in the nodes.
        2. Compute the probability distribution.
        3. Set the buckets dict on the graph.
        4. Return the buckets dict.

        random for the NAs according to proportion
        separate bucket
        -> ENUM for strategies
        """

        buckets = {}

        self.buckets = buckets