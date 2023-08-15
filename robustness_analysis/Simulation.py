from .DiGraph import DiGraph
from .Perturbation import Perturbation
from .AttackStrategy import AttackStrategy

class Simulation():

    def __init__(self, graph: DiGraph, k: int, attack_strategy: AttackStrategy, threatened_habitats: list =[], threatened_species: list =[]) -> None:
        self.threatened_habitats = threatened_habitats
        self.threatened_species = threatened_species
        self.graphs = self.create_graph_copies(graph, k)
        self.perturbations = self.create_perturbations(self.graphs, k, attack_strategy)


    def create_graph_copies(self, graph: DiGraph, k: int) -> list:
        return [graph.copy() for _ in range(k)]
    

    def create_perturbations(self, graphs: list, k: int, attack_strategy: AttackStrategy) -> list:
        return [Perturbation(graphs[i], attack_strategy, self.threatened_habitats, self.threatened_species) for i in range(k)]
        

    def run(self) -> None:
        # TODO: parallelize, or if too heavy, use sequential strategy
        pass


    def get_results() -> list:
        pass