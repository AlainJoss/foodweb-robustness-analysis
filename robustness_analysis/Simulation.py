from multiprocessing import Pool, cpu_count
from .perturbation import Perturbation
from .graph import Graph
from collections import defaultdict

class Simulation():

    def __init__(self, graph: Graph, k: int) -> None:
        self.graphs = self._create_graph_copies(graph, k)
        self.perturbations = self._create_perturbations(k)


    def _create_graph_copies(self, graph: Graph, k: int) -> list:
        return [graph.copy() for _ in range(k)]
    
    
    def _create_perturbations(self, k: int) -> list:
        return [Perturbation(self.graphs[i]) for i in range(k)]
    
    
    def run(self) -> None:
        # Use all available CPU cores
        num_processes = cpu_count()
        
        # Parallelize with multiprocessing and capture metric evolutions
        with Pool(processes=num_processes) as pool:
            self.metric_evolutions = pool.map(self._run_perturbation, self.perturbations)

        
    @staticmethod
    def _run_perturbation(perturbation: Perturbation) -> dict:
        """
        Helper method to run a single perturbation.
        
        Parameters:
        -----------
        perturbation : Perturbation
            The perturbation instance to be run.
        
        Returns:
        --------
        dict
            Metric evolution of the perturbed graph.
        """
        perturbation.run()
        return perturbation.graph.get_metric_evolution()


    def get_results(self) -> dict:
        # Initialize total_results with empty lists
        total_results = defaultdict(list)

        # Summing results from all perturbations
        for metric_evolution in self.metric_evolutions:
            for key, value_list in metric_evolution.items():
                if key not in total_results:
                    total_results[key] = [0] * len(value_list)
                total_results[key] = [sum(x) for x in zip(total_results[key], value_list)]

        # Divide by the number of perturbations to compute the average
        num_perturbations = len(self.metric_evolutions)
        averaged_dict = {key: [v / num_perturbations for v in value_list] for key, value_list in total_results.items()}
        
        return averaged_dict

