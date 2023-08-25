# Food Web Robustness Analysis

This project aims to decipher the intricacies of Switzerland's food web by analyzing its robustness under different perturbation techniques.

## 🌟 **Objective**

The primary objective of this project is to:
- Apply various attack strategies to simulate perturbations.
- Extract results for analysis.

## 📚 **Modules Overview**

### 1. `constants.py`
- Houses constants and configurations used throughout the project.

### 2. `attack_strategy.py`
- Defines various attack strategies for perturbing the graph.
- Includes strategies like RANDOM, SEQUENTIAL, THREATENED_HABITATS, and THREATENED_SPECIES.

### 3. `metaweb.py`
- The `Metaweb` class resides here, responsible for data acquisition and preprocessing.

### 4. `graph.py`
- This module represents the food web using a directed graph.
- Provides utilities for graph manipulation and metric computation.

### 5. `metric_calculator.py`
- Contains the MetricCalculator class responsible for computing various metrics on the graph.

### 6. `perturbation.py`
- Represents a perturbation process on a graph where nodes are removed, and metrics are updated at each step.

### 7. `simulation.py`
- The core simulation module that uses different attack strategies on the graph and computes metrics.

### 8. `random_simulation.py`
- Specialized simulation using the random attack strategy.

### 9. `sequential_simulation.py`
- Specialized simulation using the sequential attack strategy.

### 10. `threatened_habitats_simulation.py`
- Specialized simulation considering threatened habitats.

### 11. `threatened_species_simulation.py`
- Specialized simulation focusing on threatened species.

### 12. `file_exporter.py`
- Utility module for exporting data and results.

## 🔍 **Running the Simulations**

- Use the respective simulation files (`random_simulation.py`, `sequential_simulation.py`, etc.) to run simulations with different strategies.
- Ensure all dependencies are installed and data files are available.
