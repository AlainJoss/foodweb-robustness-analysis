import sys
sys.path.append('../')

from graph import Graph
from metaweb import Metaweb, MetawebProcessor
from attack_strategy import Random
from metaweb import ProcessingStrategy
from simulation import Simulation
import constants
from file_exporter import export


if __name__ == "__main__":

    # setup edges 
    metaweb_processor = MetawebProcessor(constants.ALL_SPECIES_AND_FOOD_GROUPS, constants.SPECIES_FOR_RANDOMIZED_LINKS)
    metaweb = Metaweb(constants.FOODWEB_02, usecols=[constants.SOURCE_COL, constants.TARGET_COL])
    metaweb.setup(ProcessingStrategy.USE_AS_IS, metaweb_processor)
    edge_df = metaweb.get_edges()

    # setup graph
    attack_strategy = Random()
    graph = Graph(attack_strategy, edge_df, source=constants.SOURCE_COL, target=constants.TARGET_COL)
    graph.setup_attack_strategy()

    # run simulation
    simulation = Simulation(graph, 2)
    simulation.run()

    simulation_results = simulation.get_results()

    export(simulation_results, "random_simulation")
