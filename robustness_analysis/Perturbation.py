from DiGraph import DiGraph
from Enums import AttackStrategy

class Perturbation():
    def __init__(self, graph: DiGraph, attack_strategy: AttackStrategy, threatened_habitats: list =[], threatened_species: list =[]) -> None:
        self.graph = graph
        self._create_buckets(attack_strategy, threatened_habitats, threatened_species)
        self.metric_trend = {metric.__name__: [] for metric in self.graph.metrics}


    def _create_buckets(self, attack_strategy: AttackStrategy, threatened_habitats: list =[], threatened_species: list = []) -> None:
        if attack_strategy == AttackStrategy.RANDOM:
            self.graph.create_random_buckets()
        elif attack_strategy == AttackStrategy.SEQUENTIAL:
            self.graph.create_sequential_buckets()
        elif attack_strategy == AttackStrategy.THREATENED_HABITATS:
            self.graph.create_threatened_habitats_buckets(threatened_habitats)
        elif attack_strategy == AttackStrategy.THREATENED_SPECIES:
            self.graph.create_threatened_species_buckets(threatened_species)
        else:
            raise ValueError(f"Invalid attack strategy: {attack_strategy}")


    def run(self) -> None:
        while self.graph.size() > 0:
            computed_metrics = self.graph.compute_metrics()
            for metric in self.metric_trend:
                self.metric_trend[metric].append(computed_metrics[metric])
            
            node = self.graph.choose_node()
            self.graph.node_removal(node)


    def get_results(self) -> dict:
        return self.metric_trend



