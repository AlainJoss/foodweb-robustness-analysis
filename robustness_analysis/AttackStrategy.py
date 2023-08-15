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
        pass


class ThreatenedHabitats(AttackStrategy):

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        pass


class ThreatenedSpecies(AttackStrategy):

    def create_buckets(self, graph: nx.DiGraph) -> dict:
        pass

