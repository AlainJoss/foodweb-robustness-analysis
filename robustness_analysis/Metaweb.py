import pandas as pd
import numpy as np
import random
from Enums import Preparation


class Metaweb():
    def __init__(self, csv: str) -> None:
        self.edge_df = pd.read_csv(csv)

    def get_edge_df(self) -> pd.DataFrame:
        return self.edge_df

    def prepare(self, *, preparation: Preparation):
        if preparation == Preparation.PREPARE:
            self.create_random_links()
            self.remove_random_links()
        elif preparation == Preparation.USE_AS_IS:
            pass
        else:
            raise ValueError(f"Invalid preparation: {preparation}")

    def create_random_links(self) -> None:
        def load_dataframe_from_csv(path):
            return pd.read_csv(path)
        
        def explode_multivalue_columns(df, columns_to_explode):
            for column in columns_to_explode:
                df[column] = df[column].str.split('; ')
                df = df.explode(column)
            return df

        def filter_subdiet_by_habitat_and_zone(nodes_df, species_info):
            sub_diet = nodes_df[nodes_df[species_info['Diet_Rank']] == species_info['Diet_Name']]
            return sub_diet[(sub_diet['Habitat'] == species_info['Habitat']) & (sub_diet['Zone'] == species_info['Zone'])]

        def construct_linkage_dataframe(species_info, sub_diet_filtered):
            linkage_dataframe = pd.DataFrame(columns=['Diet_Range', 'Source', 'Target'])
            number_of_rows = len(sub_diet_filtered)
            linkage_dataframe['Source'] = np.full((number_of_rows), species_info['Taxon'])
            linkage_dataframe['Diet_Range'] = np.full((number_of_rows), species_info['Diet_Range'])
            linkage_dataframe['Target'] = sub_diet_filtered['Taxon'].values
            return linkage_dataframe

        def sample_rows_based_on_diet_range(species_group):
            if species_group['Diet_Range'].iloc[0] == 'Generalised':
                return species_group.head(int(np.ceil(0.05*len(species_group))))
            else: # assuming other category is 'Specialised'
                return species_group.sample(min(len(species_group), random.randint(1, 5)))

        def generate_links(nodes_df, random_species_links_df):
            all_possible_links = pd.DataFrame(columns=['Diet_Range', 'Source', 'Target'])
            
            for i in range(len(random_species_links_df)):
                species_info = random_species_links_df.iloc[i]
                sub_diet_filtered = filter_subdiet_by_habitat_and_zone(nodes_df, species_info)
                linkage_dataframe = construct_linkage_dataframe(species_info, sub_diet_filtered)
                all_possible_links = pd.concat([all_possible_links, linkage_dataframe])

            all_possible_links = all_possible_links.drop_duplicates(subset=['Source', 'Target'])
            return all_possible_links.groupby('Source').apply(sample_rows_based_on_diet_range).reset_index(drop=True)

        node_list_dataframe = load_dataframe_from_csv('../node_lists/all_species_and_feeding_groups.csv')
        node_list_dataframe = explode_multivalue_columns(node_list_dataframe, ['Habitat', 'Zone'])

        random_species_links_dataframe = load_dataframe_from_csv('../node_lists/species_for_randomized_links.csv')
        random_species_links_dataframe = explode_multivalue_columns(random_species_links_dataframe, ['Habitat', 'Zone'])

        sampled_links = generate_links(node_list_dataframe, random_species_links_dataframe)

        # Add edges to G
        G = "Network"
        for i in range(len(sampled_links)):
            edge = sampled_links[i]
            source = edge['Source']
            target = edge['Target']
            G.add_edge(source, target)
            

    def remove_random_links(self) -> None:
        def remove_links(G, k_threshhold, percentage_to_remove=0.9):
            nodes = list(G.nodes)
            for node in nodes:
                in_degree = G.in_degree(node)

                if in_degree >= k_threshhold:
                    inward_edges = list(G.in_edges(node))
                    num_edges_to_remove = int(in_degree * percentage_to_remove)
                    edges_to_remove = random.sample(inward_edges, num_edges_to_remove)
                    G.remove_edges_from(edges_to_remove)
            return G

        # usage
        threshold_k = 10
        G = remove_links(G, threshold_k)
