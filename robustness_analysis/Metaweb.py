import pandas as pd
import numpy as np
import random
from enum import Enum

class Preparation(Enum):
    USE_AS_IS = "use_as_is"
    PREPARE = "prepare"

class DataProcessor:
    """
    Utility class for processing node and link data, generating linkages, 
    and managing node attributes like habitat and feeding types.
    """
    def __init__(self, nodes_path: str, links_path: str):
        self.nodes = pd.read_csv(nodes_path)
        self.links = pd.read_csv(links_path)
        self._explode_columns(['Habitat', 'Zone'])

    def _explode_columns(self, columns: list):
        for column in columns:
            self.nodes[column] = self.nodes[column].str.split('; ')
            self.nodes = self.nodes.explode(column)
            self.links[column] = self.links[column].str.split('; ')
            self.links = self.links.explode(column)

    def generate_links(self):
        """
        Generates linkage data based on the provided nodes and links data.
        
        Parameters:
        -----------
        nodes : pandas.DataFrame
            DataFrame containing node data.
        links : pandas.DataFrame
            DataFrame containing link data.
        
        Returns:
        --------
        pandas.DataFrame
            The generated linkage data.
        """
        all_links = pd.DataFrame(columns=['Diet_Range', 'Source', 'Target'])

        for _, species in self.links.iterrows():
            filtered_diet = self._filter_by_habitat_and_zone(species)
            linkage_data = self._create_linkage_data(species, filtered_diet)
            all_links = pd.concat([all_links, linkage_data])

        all_links = all_links.drop_duplicates(subset=['Source', 'Target'])
        return all_links.groupby('Source').apply(self._sample_based_on_diet).reset_index(drop=True)

    def _filter_by_habitat_and_zone(self, species):
        sub_diet = self.nodes[self.nodes[species['Diet_Rank']] == species['Diet_Name']]
        return sub_diet[(sub_diet['Habitat'] == species['Habitat']) & (sub_diet['Zone'] == species['Zone'])]

    def _create_linkage_data(self, species, filtered_diet):
        linkage_data = pd.DataFrame(columns=['Diet_Range', 'Source', 'Target'])
        num_rows = len(filtered_diet)
        linkage_data['Source'] = np.full((num_rows), species['Taxon'])
        linkage_data['Diet_Range'] = np.full((num_rows), species['Diet_Range'])
        linkage_data['Target'] = filtered_diet['Taxon'].values
        return linkage_data

    def _sample_based_on_diet(self, species_group, percentage=0.05):
        if species_group['Diet_Range'].iloc[0] == 'Generalised':
            return species_group.head(int(np.ceil(percentage*len(species_group))))
        else:
            return species_group.sample(min(len(species_group), random.randint(1, 5)))

class Metaweb:
    """
    Represents the metaweb, essentially the directed graph of species interactions.
    Provides methods to prepare the metaweb and manage its edges.
    """
    def __init__(self, csv: str, usecols: list):
        self.edges = pd.read_csv(csv, usecols=usecols)

    def get_edges(self) -> pd.DataFrame:
        return self.edges

    def prepare(self, preparation: Preparation, data_processor: DataProcessor):
        """
        Prepares the metaweb based on the given preparation type.
        
        Parameters:
        -----------
        preparation_type : Preparation (Enum)
            The type of preparation to apply to the metaweb.
        """
        if preparation == Preparation.PREPARE:
            self._add_random_links(data_processor)
            self._remove_random_links()

    def _add_random_links(self, data_processor: DataProcessor):
        new_links = data_processor.generate_links()
        self.edges = pd.concat([self.edges, new_links]).reset_index(drop=True)

    def _remove_random_links(self, threshold=10, percentage=0.9):
        nodes = self.edges['Source'].unique()
        for node in nodes:
            in_degree = self.edges[self.edges['Target'] == node].shape[0]

            if in_degree >= threshold:
                inward_edges = self.edges[self.edges['Target'] == node]
                num_to_remove = int(in_degree * percentage)
                to_remove = inward_edges.sample(num_to_remove)
                self.edges = self.edges.drop(to_remove.index)
