from DiGraph import DiGraph
from BucketContainer import BucketContainer
import random

class Perturbation():
    def __init__(self, graph: DiGraph) -> None:
        self.graph = graph
        self.bucket_container = BucketContainer()

    def set_lost_habitats(self, lost_habitats: list) -> None:
        self.lost_habitats = lost_habitats

    def choose_bucket(self) -> object:
        return random.choices
    
    def run(self) -> None:
        bucket = self.choose_bucket()
        node = bucket.

