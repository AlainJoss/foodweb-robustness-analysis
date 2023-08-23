from graph import Graph
from metaweb import Metaweb, MetawebProcessor
from attack_strategy import ThreatenedHabitats
from metaweb import Preparation
from simulation import Simulation
import paths as Constants
import pandas as pd


def main():
    metaweb_processor = MetawebProcessor(Constants.ALL_SPECIES_AND_FOOD_GROUPS, Constants.SPECIES_FOR_RANDOMIZED_LINKS)
    metaweb = Metaweb(Constants.FOODWEB_02, usecols=[Constants.SOURCE_COL, Constants.TARGET_COL])
    metaweb.prepare(Preparation.GENERATE_AND_REMOVE, metaweb_processor)
    edge_df = metaweb.get_edges()

    graph = Graph(edge_df, source=Constants.SOURCE_COL, target=Constants.TARGET_COL)
    species_df = pd.read_csv(Constants.ALL_SPECIES_AND_FOOD_GROUPS, usecols=['Taxon', 'Habitat'])
    graph.update_attributes(species_df)

    threatened_habitats = ["Grassland", "Forest"]
    attack_strategy = ThreatenedHabitats(threatened_habitats)
    attack_strategy.create_buckets(graph)

    simulation = Simulation(graph, 10)
    simulation.run()

    results = simulation.get_results()
    print(results)  


if __name__ == "__main__":
    main()
