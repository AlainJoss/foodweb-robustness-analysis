from multiprocessing import Pool, cpu_count
from perturbation import Perturbation
from graph import Graph
from collections import defaultdict


class Simulation():
    
    def __init__(self, graph: Graph, k: int) -> None:
        # TODO: create copies only for metaweb 02, create different graphs for 03
        self.graphs = self._create_graph_copies(graph, k)
        self.perturbations = self._create_perturbations(k)


    def _create_graph_copies(self, graph: Graph, k: int) -> list:
        return [graph.copy() for _ in range(k)]
    
    
    def _create_perturbations(self, k: int) -> list:
        return [Perturbation(i, self.graphs[i]) for i in range(k)]
    
    
    def run(self) -> None:
        # Use all available CPU cores
        num_processes = cpu_count()
        
        # Parallelize with multiprocessing and capture metric evolutions
        with Pool(processes=num_processes) as pool:
            self.metric_evolution = pool.map(self._run_perturbation, self.perturbations)

        # Expand each metric evolution
        for idx, metric_evolution in enumerate(self.metric_evolution):
            self.metric_evolution[idx] = self._expand_list_based_on_graph_size(metric_evolution)
    
        
    @staticmethod
    def _run_perturbation(perturbation: Perturbation) -> dict:
        """
        Helper method to run a single perturbation.
        """
        perturbation.run()
        return perturbation.get_metric_evolution()
    

    def get_results(self) -> dict:
        # Initialize total_results with empty lists
        total_results = defaultdict(list)

        # Summing results from all perturbations
        for metric_evolution in self.metric_evolution:
            for key, value_list in metric_evolution.items():
                if key not in total_results:
                    total_results[key] = [0] * len(value_list)
                total_results[key] = [sum(x) for x in zip(total_results[key], value_list)]

        # Divide by the number of perturbations to compute the average
        num_perturbations = len(self.metric_evolution)
        averaged_dict = {key: [v / num_perturbations for v in value_list] for key, value_list in total_results.items()}
        
        return averaged_dict
        

    def _expand_list_based_on_graph_size(self, metric_evolution: dict) -> dict:
        graph_size_list = metric_evolution['graph_size']
        expanded_dict = defaultdict(list)
        
        for i in range(len(graph_size_list) - 1):
            diff = graph_size_list[i] - graph_size_list[i+1] - 1
            for key, value_list in metric_evolution.items():
                for _ in range(diff + 1):  # +1 to include the current time step as well
                    expanded_dict[key].append(value_list[i])

        # Add the last values since they don't have a "next" value for comparison
        for key, value_list in metric_evolution.items():
            expanded_dict[key].append(value_list[-1])

        return expanded_dict