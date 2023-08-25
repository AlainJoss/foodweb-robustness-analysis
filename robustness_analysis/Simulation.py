from multiprocessing import Pool, cpu_count
from perturbation import Perturbation
from graph import Graph
from collections import defaultdict

class Simulation():
    """
    Simulates the perturbation process on multiple copies of a graph.
    
    Attributes:
    -----------
    graphs : list
        List of graph copies on which perturbations will be performed.
    perturbations : list
        List of perturbation instances associated with each graph copy.
    metric_evolution : list
        List of metric evolutions for each perturbation.
    """

    def __init__(self, graph: Graph, k: int) -> None:
        """
        Initializes the Simulation with graph copies and perturbations.
        
        Parameters:
        -----------
        graph : Graph
            The graph on which perturbations will be simulated.
        k : int
            The number of graph copies and perturbations.
        """
        self.graphs = self._create_graph_copies(graph, k)
        self.perturbations = self._create_perturbations(k)


    def _create_graph_copies(self, graph: Graph, k: int) -> list:
        """
        Creates k copies of the provided graph.
        
        Parameters:
        -----------
        graph : Graph
            The graph to be copied.
        k : int
            The number of copies to create.
        
        Returns:
        --------
        list
            A list of graph copies.
        """
        return [graph.copy() for _ in range(k)]
    

    def _create_perturbations(self, k: int) -> list:
        """
        Creates k perturbations for the graph copies.
        
        Parameters:
        -----------
        k : int
            The number of perturbations to create.
        
        Returns:
        --------
        list
            A list of Perturbation instances.
        """
        return [Perturbation(i, self.graphs[i]) for i in range(k)]
    

    def run(self) -> None:
        """
        Runs the simulation in parallel for all perturbations using available CPU cores.
        """
        num_processes = cpu_count()
        
        with Pool(processes=num_processes) as pool:
            self.metric_evolution = pool.map(self._run_perturbation, self.perturbations)
    

    @staticmethod
    def _run_perturbation(perturbation: Perturbation) -> dict:
        """
        Helper method to run a single perturbation.
        
        Parameters:
        -----------
        perturbation : Perturbation
            The perturbation instance to run.
        
        Returns:
        --------
        dict
            The metric evolution for the perturbation.
        """
        perturbation.run()
        return perturbation.get_metric_evolution()


    def get_results(self) -> dict:
        """
        Aggregates and averages the results from all perturbations.
        
        Returns:
        --------
        dict
            The averaged metric evolution over all perturbations.
        """
        total_results = defaultdict(list)

        for metric_evolution in self.metric_evolution:
            for key, value_list in metric_evolution.items():
                if key not in total_results:
                    total_results[key] = [0] * len(value_list)
                total_results[key] = [sum(x) for x in zip(total_results[key], value_list)]

        num_perturbations = len(self.metric_evolution)
        averaged_dict = {key: [v / num_perturbations for v in value_list] for key, value_list in total_results.items()}
        
        return averaged_dict
