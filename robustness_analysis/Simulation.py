from DiGraph import DiGraph
from enum import Enum
from Perturbation import Perturbation

class AttackStrategy(Enum):
    RANDOM = "random"
    SEQUENTIAL = "sequential"
    LOST_HABITATS = "lost_habitats"
    THREATENED_SPECIES = "threatened_species"

class Simulation():
    def __init__(self, graph: DiGraph, k: int, attack_strategy: AttackStrategy) -> None:
        self.graphs = self.create_graph_copies(graph, k)
        self.perturbations = self.create_perturbations(self.graphs, attack_strategy)

    def create_graph_copies(self, graph: DiGraph, k: int) -> list:
        return [graph.copy() for i in range(k)]

    def create_perturbations(self, graphs: list, k: int, attack_strategy: AttackStrategy) -> list:
        return [Perturbation(graphs[i]) for i in range(k)]
        

    def run(self) -> None:
        pass

    def get_results() -> list:
        pass