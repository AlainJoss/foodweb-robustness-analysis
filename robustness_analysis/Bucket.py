import random

class Bucket():
    def __init__(self, nodes: list) -> None:
        self.nodes = nodes

    def get_random_node(self) -> object:
        return random.choice(self.nodes)