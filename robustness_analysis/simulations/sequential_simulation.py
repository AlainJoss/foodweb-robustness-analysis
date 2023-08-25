import sys
sys.path.append('../')

from graph import Graph
from metaweb import Metaweb, MetawebProcessor
from attack_strategy import Sequential
from metaweb import ProcessingStrategy
from simulation import Simulation
import constants
from file_exporter import export


if __name__ == "__main__":

    print(">>> setting up simulation")

    ##### setup edges #####

    metaweb_processor = MetawebProcessor(constants.ALL_SPECIES_AND_FOOD_GROUPS, constants.SPECIES_FOR_RANDOMIZED_LINKS)
    metaweb = Metaweb(constants.FOODWEB_02, usecols=[constants.SOURCE_COL, constants.TARGET_COL])

    # user TODO: set strategy: ProcessingStrategy = USE_AS_IS, REMOVE, GENERATE_AND_REMOVE

    metaweb.setup(strategy=ProcessingStrategy.USE_AS_IS, data_processor=metaweb_processor)
    edge_df = metaweb.get_edges()

    ##### setup graph #####

    # user TODO: set metric: Sequential.SortBy = metric to sort nodes with: DEGREE, BETWEENNESS, CLOSENESS, ...

    attack_strategy = Sequential(metric=Sequential.SortBy.DEGREE)
    graph = Graph(attack_strategy, edge_df, source=constants.SOURCE_COL, target=constants.TARGET_COL)
    graph.setup_attack_strategy()

    ##### run simulation #####

    # user TODO: set save_nodes: bool = whether to track primary removals

    simulation = Simulation(graph, 1, save_nodes=True)
    simulation.run()