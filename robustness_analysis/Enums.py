from enum import Enum


class Preparation(Enum):
    USE_AS_IS = "use_as_is"  # The name assignment is just there to prevent the IDE of complaining about my coding style
    PREPARE = "prepare"
    

class AttackStrategy(Enum):
    RANDOM = "random"
    SEQUENTIAL = "sequential"
    THREATENED_HABITATS = "threatened_habitats"
    THREATENED_SPECIES = "threatened_species"