import networkx as nx
from enum import Enum

class Metrics(Enum):
    """
    Enumeration of available graph metrics.
    """
    GRAPH_SIZE = "graph_size"
    AVG_IN_DEGREE = "avg_in_degree"
    AVG_OUT_DEGREE = "avg_out_degree"
    AVG_TOTAL_DEGREE = "avg_total_degree"
    DENSITY = "density"
    NUMBER_OF_WCCS = "number_of_wccs"


class MetricCalculator():
    """
    Utility class to compute various metrics for directed graphs.
    
    Attributes:
    -----------
    METRICS : list of str
        List of metric method names available in this class.
    """
    
    METRICS = [metric.value for metric in Metrics]
    
    def compute_metrics(self, graph: nx.DiGraph) -> dict:
        """
        Computes all the metrics listed in METRICS for the provided graph.
        
        Parameters:
        -----------
        graph : nx.DiGraph
            The graph for which metrics are to be calculated.
        
        Returns:
        --------
        dict
            Dictionary with metric names as keys and computed values as associated values.
        """
        metric_results = {}
        DECIMAL_POS = 5  # decimal precision
        
        for metric in self.METRICS:
            metric_function = getattr(self, metric)
            metric_results[metric] = round(metric_function(graph), DECIMAL_POS)  
        
        return metric_results
    

    def graph_size(self, graph:nx.DiGraph) -> float:
        return len(graph)
    

    def avg_in_degree(self, graph: nx.DiGraph) -> float:
        return sum(dict(graph.in_degree()).values()) / len(graph)
    
    
    def avg_out_degree(self, graph: nx.DiGraph) -> float:
        return sum(dict(graph.out_degree()).values()) / len(graph)
    
    
    def avg_total_degree(self, graph: nx.DiGraph) -> float:
        return sum(dict(graph.degree()).values()) / len(graph)

    
    def density(self, graph: nx.DiGraph) -> float:
        n = len(graph) 
        if n < 2:
            return 0  # or some other value to indicate the graph is too small
        return nx.density(graph)
    

    def largest_wcc_size(self, graph: nx.DiGraph) -> float:
        return len(max(list(nx.weakly_connected_components(graph))))

    
    def largest_ssc_size(self, graph: nx.DiGraph) -> float:
        return len(max(list(nx.strongly_connected_components(graph))))
    

    def number_of_wccs(self, graph: nx.DiGraph) -> float:
        return len(list(nx.weakly_connected_components(graph)))
    
    
    def number_of_sccs(self, graph: nx.DiGraph) -> float:
        return len(list(nx.strongly_connected_components(graph)))
    
    
    def avg_pagerank(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.pagerank(graph)).values()) / len(graph)
    
    
    def avg_betweenness(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.betweenness_centrality(graph, normalized=False)).values())
    

    def avg_in_closeness(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.closeness_centrality(graph, normalized=False)).values())
    

    def avg_shortest_path_lssc(self, graph: nx.DiGraph) -> float:
        lscc = max(nx.strongly_connected_components(graph), key=len)
        subgraph = graph.subgraph(lscc)
        return nx.average_shortest_path_length(subgraph)


    def avg_trophic_level(self, graph: nx.DiGraph) -> float:
        return sum(dict(nx.trophic_levels(graph)).values()) / len(graph)
