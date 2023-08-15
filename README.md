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

### 2. `Enums.py`
- Enumerations central to the project, such as `AttackStrategy` which encompasses strategies like RANDOM, SEQUENTIAL, THREATENED_HABITATS, and THREATENED_SPECIES.

### 3. `Metaweb.py`
- The `Metaweb` class resides here, responsible for data acquisition and preprocessing.

### 4. `DiGraph.py`
- This module is the backbone of our food web representation.
- Uses NetworkX for graph modeling and manipulation.
- Features include computing graph metrics, node removal based on strategies, and bucket creation for node selection.

### 5. `Perturbation.py`
- The `Perturbation` class implements node removal based on different strategies.
- It records the trend of graph metrics over time, providing insights into the impact of perturbations.

### 6. `Simulation.py`
- Orchestrates the entire simulation process, binding all other modules together for a cohesive workflow.

## 📘 **Jupyter Notebooks**

- **`perturubation.ipynb`**: A detailed deep dive into the perturbation process with visualizations.
- **`simulations.ipynb`**: A broader view, showcasing various simulations and their outcomes.

## 🔧 **Setting Up**

1. Clone this repository to your local machine.
2. Make sure you have the required libraries: NetworkX, Pandas, NumPy, and Matplotlib.
3. Open the Jupyter notebooks to understand the workflow and run simulations.

## 🚀 **Future Goals**

- Integrate the remaining attack strategies.
- Integrate the preparation routine of the metaweb.
- Integrate more network metrics to track during perturbations.
- Write the simulation code, to run multiple perturbations in parallel.
- Create visualizations and gifs for data interpretation.

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
