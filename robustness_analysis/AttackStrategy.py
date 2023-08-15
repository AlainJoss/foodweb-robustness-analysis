from abc import ABC, abstractmethod
import networkx as nx

class AttackStrategy(ABC):

    @abstractmethod
    def create_buckets(self, graph: nx.DiGraph) -> dict:
        pass

class Random(AttackStrategy):

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        for node in graph.nodes():
            graph.nodes[node]['bucket'] = 'b1'
        return {'b1': 1.0}

class Sequential(AttackStrategy):

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        # Implementation here
        pass

class ThreatenedHabitats(AttackStrategy):

    def __init__(self, threatened_habitats: list = None):
        if threatened_habitats is None:
            self.threatened_habitats = []
        else:
            self.threatened_habitats = threatened_habitats

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        # Use self.threatened_habitats in the implementation
        pass

class ThreatenedSpecies(AttackStrategy):

    def __init__(self, threatened_species: list = None):
        if threatened_species is None:
            self.threatened_species = []
        else:
            self.threatened_species = threatened_species

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        # Use self.threatened_species in the implementation
        pass

