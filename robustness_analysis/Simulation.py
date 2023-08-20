from multiprocessing import Pool
from .perturbation import Perturbation
from .graph import Graph

class Simulation():

    def __init__(self, graph: Graph, k: int) -> None:
        self.graphs = self._create_graph_copies(graph, k)
        self.perturbations = self._create_perturbations(k)

    def _create_graph_copies(self, graph: Graph, k: int) -> list:
        return [graph.copy() for _ in range(k)]
    
    def _create_perturbations(self, k: int) -> list:
        return [Perturbation(self.graphs[i]) for i in range(k)]
    
    def run(self) -> None:
        # Parallelize with multiprocessing
        with Pool() as pool:
            pool.map(self._run_perturbation, self.perturbations)
    
    @staticmethod
    def _run_perturbation(perturbation: Perturbation) -> None:
        """
        Helper method to run a single perturbation.
        
        Parameters:
        -----------
        perturbation : Perturbation
            The perturbation instance to be run.
        """
        perturbation.run()

    def get_results(self) -> dict:
        # Get results dictionary from each Perturbation and average
        total_results = {}
        num_perturbations = len(self.perturbations)

        # Summing results from all perturbations
        for perturbation in self.perturbations:
            results = perturbation.get_metric_evolution()
            for key, value in results.items():
                if key not in total_results:
                    total_results[key] = value
                else:
                    total_results[key] += value

        # Averaging the results
        average_results = {key: value / num_perturbations for key, value in total_results.items()}
        
        return average_results