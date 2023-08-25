import sys
sys.path.append('../')

from graph import Graph
from metaweb import Metaweb, MetawebProcessor
from attack_strategy import ThreatenedHabitats
from metaweb import ProcessingStrategy
from simulation import Simulation
import constants
from file_exporter import export

"""
Copy paste combinations for each simulation.

threatened_habitats = ['Wetland']
threatened_habitats = ['Cropland']
threatened_habitats = ['Aquatic']
threatened_habitats = ['Grassland']
threatened_habitats = ['Wetland', 'Cropland']
threatened_habitats = ['Wetland', 'Aquatic']
threatened_habitats = ['Wetland', 'Grassland']
threatened_habitats = ['Cropland', 'Aquatic']
threatened_habitats = ['Cropland', 'Grassland']
threatened_habitats = ['Aquatic', 'Grassland']
threatened_habitats = ['Wetland', 'Cropland', 'Aquatic']
threatened_habitats = ['Wetland', 'Cropland', 'Grassland']
threatened_habitats = ['Wetland', 'Aquatic', 'Grassland']
threatened_habitats = ['Cropland', 'Aquatic', 'Grassland']
threatened_habitats = ['Wetland', 'Cropland', 'Aquatic', 'Grassland']
"""


if __name__ == "__main__":

    print(">>> setting up simulation")

    ##### user TODO: setup threatened_habitats: list = habitats to remove nodes from with higher probability #####

    threatened_habitats = ["Grassland", "Forest"]  # copy paste combination in here

    ##### setup edges #####

    metaweb_processor = MetawebProcessor(constants.ALL_SPECIES_AND_FOOD_GROUPS, constants.SPECIES_FOR_RANDOMIZED_LINKS)
    metaweb = Metaweb(constants.FOODWEB_02, usecols=[constants.SOURCE_COL, constants.TARGET_COL])

    # user TODO: set strategy: ProcessingStrategy = USE_AS_IS, REMOVE, GENERATE_AND_REMOVE

    metaweb.setup(strategy=ProcessingStrategy.USE_AS_IS, data_processor=metaweb_processor)
    edge_df = metaweb.get_edges()

    ##### setup graph #####
    attack_strategy = ThreatenedHabitats(threatened_habitats)
    graph = Graph(attack_strategy, edge_df, source=constants.SOURCE_COL, target=constants.TARGET_COL)
    graph.setup_attack_strategy()

    ##### run simulation #####

    # user TODO: set k: int = number of simulations, set save_nodes: bool = whether to track primary removals

    simulation = Simulation(graph, k=1000, save_nodes=True)
    simulation.run()
