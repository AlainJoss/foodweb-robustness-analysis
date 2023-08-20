# Food Web Robustness Analysis

This project aims to decipher the intricacies of Switzerland's food web by analyzing its robustness under different perturbation techniques.

## 🌟 **Objective**

The primary objective of this project is to:
- Model the food web as a directed graph.
- Apply various attack strategies to simulate perturbations.
- Analyze and visualize the impact on graph properties.

## 📚 **Modules Overview**

### 1. `Constants.py`
- Houses constants and configurations used throughout the project.

### 2. `AttackStrategy.py`
- Defines various attack strategies for perturbing the graph.
- Includes strategies like RANDOM, SEQUENTIAL, THREATENED_HABITATS, and THREATENED_SPECIES.

### 3. `Metaweb.py`
- The `Metaweb` class resides here, responsible for data acquisition and preprocessing.

### 4. `Graph.py`
- This module represents the food web using a directed graph.
- Provides utilities for graph manipulation and metric computation.

### 5. `MetricCalculator.py`
- Contains the `MetricCalculator` class, which computes various metrics for a given graph.

### 6. `Perturbation.py`
- The `Perturbation` class implements node removal based on different strategies.
- It records the trend of graph metrics over time, providing insights into the impact of perturbations.

### 7. `Simulation.py`
- Orchestrates the entire simulation process, binding all other modules together for a cohesive workflow.

## 📘 **Jupyter Notebooks**

- **`perturubation.ipynb`**: A detailed deep dive into the perturbation process with visualizations.

## 🔧 **Setting Up**

1. Clone this repository to your local machine.
2. Make sure you have the required libraries: NetworkX, Pandas, NumPy, and Matplotlib.
3. Open the Jupyter notebook (`perturubation.ipynb`) to understand the workflow and run simulations.

## 🚀 **Future Goals**

- Further improve modularization and introduce dependency injection for enhanced maintainability.
- Enhance simulation capabilities with more metrics and visualization tools.

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.