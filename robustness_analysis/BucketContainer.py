import random

class BucketContainer():
    def __init__(self) -> None:
        self.prob_dist = None
        self.buckets = None

    def get_bucket(self) -> object:
        return random.choices(self.buckets, weights=self.prob_dist, k=1)[0]