from .Graph import Graph
from .Perturbation import Perturbation
from .AttackStrategy import AttackStrategy


# TODO: carefully implement the copy() of the graph

class Simulation():

    def __init__(self, graph: Graph, k: int, attack_strategy: AttackStrategy, threatened_habitats: list =[], threatened_species: list =[]) -> None:
        self.graphs = self._create_graph_copies(graph, k)
        self.perturbations = self._create_perturbations(self.graphs, k, attack_strategy)


    def _create_graph_copies(self, graph: Graph, k: int) -> list:
        return [graph.copy() for _ in range(k)]
    

    def _create_perturbations(self, graphs: list, k: int, attack_strategy: AttackStrategy) -> list:
        return [Perturbation(graphs[i], attack_strategy, self.threatened_habitats, self.threatened_species) for i in range(k)]
        

    def run(self) -> None:
        # TODO: parallelize, or if too heavy, use sequential strategy
        pass


    def get_results() -> list:
        pass