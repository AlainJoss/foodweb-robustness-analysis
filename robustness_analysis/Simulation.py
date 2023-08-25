from multiprocessing import Pool, cpu_count
from perturbation import Perturbation
from graph import Graph
from file_exporter import export
import shutil
import os

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

    def __init__(self, graph: Graph, k: int, save_nodes: bool = False) -> None:
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
        self.perturbations = self._create_perturbations(k, save_nodes)


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
    

    def _create_perturbations(self, k: int, save_nodes: bool) -> list:
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
        return [Perturbation(i, self.graphs[i], save_nodes) for i in range(k)]
    

    def run(self) -> None:
        """
        Runs the simulation in parallel for all perturbations using available CPU cores.
        """
        print(">>> simulation started")

        remove_results_dir()

        num_processes = cpu_count()
        
        with Pool(processes=num_processes) as pool:
            self.metric_evolution = pool.map(self._run_perturbation, self.perturbations)

        print(">>> the simulation has successfully concluded, all perturbations are saved in the results directory")
    

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
        metrics_evolution = perturbation.get_metric_evolution()
        export(metrics_evolution, f'perturbation_{perturbation.id}')
        return metrics_evolution
    

def remove_results_dir() -> None:
    directory_path = "results"
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
