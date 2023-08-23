from abc import ABC, abstractmethod
import networkx as nx
from .graph import Graph

class AttackStrategy(ABC):
    """
    Abstract base class representing various strategies to attack or perturb a graph.
    Implementations of this class should define methods to categorize nodes in a graph 
    based on certain criteria or configurations.
    """

    @abstractmethod
    def create_buckets(self, graph: Graph) -> dict:
        pass

class Random(AttackStrategy):

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        for node in graph.nodes():
            graph.nodes[node]['bucket'] = 'b1'
        return {'b1': 1.0}
    
class Sequential(AttackStrategy):

    def create_buckets(self, graph: Graph) -> dict:
        # Calculate out-degrees for each node
        out_degrees = dict(graph.get_nx_graph().out_degree())
        
        # Sort nodes based on their out-degrees in descending order
        sorted_nodes = sorted(out_degrees, key=out_degrees.get, reverse=True)
        
        # Assign each node to its own bucket based on its order
        for index, node in enumerate(sorted_nodes):
            graph.get_nx_graph().nodes[node]['bucket'] = f'b{index+1}'

        # Return a dictionary where each node has its own bucket
        return {f'b{index+1}': 1/len(sorted_nodes) for index in range(len(sorted_nodes))}


class ThreatenedHabitats(AttackStrategy):

    def __init__(self, threatened_habitats: list = None, min_probability: int = 0.05):
        if threatened_habitats is None:
            self.threatened_habitats = []
        else:
            self.threatened_habitats = threatened_habitats
        self.min_probability = min_probability

    def create_buckets(self, graph: Graph) -> dict:

        nx_graph = graph.get_nx_graph()

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

        # TODO: do something here about the feeding groups

        print("Buckets after creation:", buckets)

        graph.set_buckets(buckets)

        print("Buckets set in graph:", graph.buckets)

class ThreatenedSpecies(AttackStrategy):

    def __init__(self, threatened_species: list = None):
        if threatened_species is None:
            self.threatened_species = []
        else:
            self.threatened_species = threatened_species

    def create_buckets(self, graph: Graph) -> dict:
        """
        1. Assign to each node the category according to the information in the nodes.
        2. Compute the probability distribution.
        3. Set the buckets dict on the graph.
        4. Return the buckets dict.

        random for the NAs according to proportion
        separate bucket
        -> ENUM for strategies
        """
        nx_graph = graph.get_nx_graph()

        buckets = {}

        graph.set_buckets(buckets)