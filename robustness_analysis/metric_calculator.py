import networkx as nx


class MetricCalculator():
    """
    Utility class to calculate various metrics for directed graphs.
    
    Attributes:
    -----------
    METRICS : list of str
        List of metric method names available in this class.
    """

    METRICS = [
        "graph_size",
        #"avg_in_degree",
        #"avg_out_degree",
        #"avg_total_degree",
        #"density",
        "largest_wcc_size",
        #"largest_ssc_size",
        "number_of_wccs",
        #"number_of_sccs",
        #"avg_pagerank",
        #"avg_betweenness",
        #"avg_in_closeness",
        #"avg_shortest_path_lssc",
        #"avg_trophic_level"  # NetworkXError: Trophic levels are only defined for graphs where every node has a path from a basal node (basal nodes are nodes with no incoming edges).
    ]


    @classmethod
    def get_metric_names(cls) -> list:
        return cls.METRICS
    

    def compute_metrics(self, graph: nx.DiGraph) -> dict:
        """
        Computes all the metrics listed in METRICS for a given graph.
        
        Parameters:
        -----------
        graph : AbstractGraph (or appropriate type)
            The graph for which metrics are to be computed.
        
        Returns:
        --------
        dict
            A dictionary with metric names as keys and computed values as values.
        """
        metric_results = {}
        
        for metric in self.METRICS:

            metric_function = getattr(self, metric)
            metric_results[metric] = metric_function(graph)
        
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
