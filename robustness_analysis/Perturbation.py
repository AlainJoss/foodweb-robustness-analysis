from DiGraph import DiGraph
from Simulation import AttackStrategy

class Perturbation():
    def __init__(self, graph: DiGraph, attack_strategy: AttackStrategy, threatened_habitats: list =[], threatened_species: list =[]) -> None:
        self.graph = graph
        self.graph.create_buckets(attack_strategy, threatened_habitats, threatened_species)
    
    def run(self) -> None:
        self.result = None

