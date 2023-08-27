import pandas as pd
import numpy as np
import random
from enum import Enum


class MetawebProcessor:
    """
    Utility class for adding and removing nodes from the given metaweb.
    The rules for doing so are based on information stored in the datasets passed to the MetawebProcessor.
    """

    def __init__(self, ALL_SPECIES_AND_FOOD_GROUPS: str, SPECIES_FOR_RANDOMIZED_LINKS: str):
        self.all_species = pd.read_csv(ALL_SPECIES_AND_FOOD_GROUPS)
        self.rand_link_species = pd.read_csv(SPECIES_FOR_RANDOMIZED_LINKS)
        self._explode_columns()


    def _explode_columns(self, columns: list = ["Habitat", "Zone"]):
        """
        Creates n new rows for each row with n items, separated by ";", in column "Habitat" and "Zone".
        For example, if a row had the values:
            1. Habitat: "Forest; Urban", Zone: "In vegetation; On vegetation"
    
        It would be split into four rows:
            1. Habitat: "Forest", Zone: "In vegetation"
            2. Habitat: "Forest", Zone: "On vegetation"
            3. Habitat: "Urban", Zone: "In vegetation"
            4. Habitat: "Urban", Zone: "On vegetation"
        """
        for column in columns:
            self.all_species[column] = self.all_species[column].str.split('; ')
            self.all_species = self.all_species.explode(column)
            self.rand_link_species[column] = self.rand_link_species[column].str.split('; ')
            self.rand_link_species = self.rand_link_species.explode(column)


    def generate_links(self):
        """
        Generates new links for fake basal species (species in the rand_link_species df) following these steps:
            1. Retrieve diet in same habitat and zone
            2. Appendend the diet range information
            3. Sample some of the links based on the diet range logic
            4. Drop the diet range information before returning the links to add to the metaweb.
        """
        all_links = pd.DataFrame(columns=['Diet_Range', 'Source_Name', 'Target_Name'])

        for _, species in self.rand_link_species.iterrows():
            filtered_diet = self._filter_diet_by_habitat_and_zone(species)
            new_links = self._format_links(species, filtered_diet)
            all_links = pd.concat([all_links, new_links])

        all_links = all_links.drop_duplicates(subset=['Source_Name', 'Source_Name'])
        sampled_links = all_links.groupby('Source_Name').apply(self._sample_based_on_diet).reset_index(drop=True)
        sampled_links.drop(columns="Diet_Range", inplace=True)

        return sampled_links

    def _filter_diet_by_habitat_and_zone(self, species: pd.Series) -> pd.DataFrame:
        """
        Returns the diet of a species in the rand_link_species df and filters it by habitat and zone.
        The diet is a subset of the all_species data frame.

        The function:
            1. Uses the Diet_Rank and Diet_Name of the input species to select matching species from 'all_species'.
            2. Further narrows down the selection based on Habitat and Zone of the input species.
        """

        diet_rank = species['Diet_Rank']  # Can be one of the following: [Kingdom, Phylum, Class, Order, Family, Genus]
        diet_name = species['Diet_Name']

        overall_diet = self.all_species[self.all_species[diet_rank] == diet_name]
        filtered_diet = overall_diet[(overall_diet['Habitat'] == species['Habitat']) & (overall_diet['Zone'] == species['Zone'])]
        
        return filtered_diet


    def _format_links(self, species: pd.Series, filtered_diet: pd.DataFrame):
        """
        Formats the links to return appending the Diet_Range information.
        """
        new_links = pd.DataFrame(columns=['Diet_Range', 'Source_Name', 'Target_Name'])
        num_rows = len(filtered_diet)
        
        new_links['Source_Name'] = np.full((num_rows), species['Taxon'])
        new_links['Diet_Range'] = np.full((num_rows), species['Diet_Range'])
        new_links['Target_Name'] = filtered_diet['Taxon'].values

        return new_links
    

    def _sample_based_on_diet(self, species_group, percentage=0.05):
        # TODO: check if behaviour .head() is correct.
        if species_group['Diet_Range'].iloc[0] == 'Generalised':
            return species_group.head(int(np.ceil(percentage*len(species_group))))
        else:
            return species_group.sample(min(len(species_group), random.randint(1, 5)))
    

    def remove_random_links(self, edges_df: pd.DataFrame, link_removal_percentage=0.9) -> pd.DataFrame:
        """
        Removes a given percentage of links on nodes that have an in_degree higher than the given threshhold.
        """

        in_degrees = edges_df.groupby('Target_Name').size()
        threshhold = in_degrees.median()

        nodes = edges_df['Source_Name'].unique()
        indices_to_drop = []

        for node in nodes:
            inward_edges = edges_df[edges_df['Target_Name'] == node]

            in_degree = len(inward_edges)
            if in_degree >= threshhold:
                num_to_remove = int(in_degree * link_removal_percentage)
                to_remove = inward_edges.sample(num_to_remove)
                indices_to_drop.extend(to_remove.index.tolist())

        edges_df = edges_df.drop(indices_to_drop).reset_index(drop=True)
        
        return edges_df
    

class ProcessingStrategy(Enum):
    """
    Stores different strategies that can be used to process the metaweb,
    before being used to create the graph.
    """

    USE_AS_IS = "USE_AS_IS"
    GENERATE_AND_REMOVE = "GENERATE_AND_REMOVE"
    REMOVE = "REMOVE"


class Metaweb:
    """
    Stores the metaweb and provides functionality for adding and removing links.
    The procedures for adding and removing links are implemented by the MetawebProcessor.
    """

    def __init__(self, csv: str, usecols: list) -> None:
        self.edges = pd.read_csv(csv, usecols=usecols)


    def get_edges(self) -> pd.DataFrame:
        return self.edges


    def setup(self, strategy: ProcessingStrategy, data_processor: MetawebProcessor) -> None:
        if strategy == ProcessingStrategy.GENERATE_AND_REMOVE:
            self._add_random_links(data_processor)
            self._remove_random_links(data_processor)
        elif strategy == ProcessingStrategy.REMOVE:
            self._remove_random_links(data_processor)


    def _add_random_links(self, data_processor: MetawebProcessor) -> None:
        new_edges = data_processor.generate_links()
        self.edges = pd.concat([self.edges, new_edges]).reset_index(drop=True)


    def _remove_random_links(self, data_processor: MetawebProcessor):
        self.edges = data_processor.remove_random_links(self.edges)