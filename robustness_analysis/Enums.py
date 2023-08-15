from enum import Enum


class Preparation(Enum):
    USE_AS_IS = "use_as_is"  # The name assignment is just there to prevent the IDE of complaining about my coding style
    PREPARE = "prepare"
    

class AttackStrategy(Enum):
    RANDOM = "random"
    SEQUENTIAL = "sequential"
    THREATENED_HABITATS = "threatened_habitats"
    THREATENED_SPECIES = "threatened_species"


class Metrics(Enum):
    AVG_IN_DEGREE = "avg_in_degree"
    AVG_OUT_DEGREE = "avg_out_degree"
    AVG_TOTAL_DEGREE = "avg_total_degree"
    DENSITY = "density"
    LARGEST_WCC_SIZE = "largest_wcc_size"
    LARGEST_SSC_SIZE = "largest_ssc_size"
    NUMBER_OF_WCCS = "number_of_wccs"
    NUMBER_OF_SCCS = "number_of_sccs"
    AVG_PAGERANK = "avg_pagerank"
    AVG_BETWEENNESS = "avg_betweenness"
    AVG_IN_CLOSENESS = "avg_in_closeness"
    AVG_SHORTEST_PATH_LSCC = "avg_shortest_path_lssc"
    AVG_TROPHIC_LEVEL = "avg_trophic_level"