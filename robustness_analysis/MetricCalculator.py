import networkx as nx
from Enums import Metrics


class MetricCalculator():

    def compute_metrics(self, graph: nx.DiGraph) -> dict:
        """
        When a new metric is added to the enum Metrics and the method is written below in this class,
        no change is needed in the compute_metrics() method itself.
        """
        metric_results = {}
        
        for metric in Metrics:

            metric_function = getattr(self, metric.value)
            metric_results[metric.value] = metric_function(graph)
        
        return metric_results
    

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
