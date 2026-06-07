#Combinatorial Optimization: Hybrid Metaheuristics (ACO & 2-Opt)

![Status](https://img.shields.io/badge/Status-Research_Phase-orange)
![Complexity](https://img.shields.io/badge/NP--Hard-Bypassed-red)
![License](https://img.shields.io/badge/Copyright-All_Rights_Reserved-lightgrey)

This repository contains advanced experimental research on solving NP-Hard combinatorial problems, specifically targeting the Traveling Salesperson Problem (TSP) in high-dimensional spaces. 

By avoiding naive algorithms (like brute force or simple greedy search), this project implements a **Hybrid Metaheuristic Algorithm** combining **Ant Colony Optimization (ACO)** with a **2-Opt Local Search** for local minima escape and rapid convergence.

## Algorithmic Architecture

### 1. Pheromone Matrix & State Transition (ACO)
The algorithm simulates biological swarm intelligence. The probability $p_{ij}^k$ of an ant $k$ moving from node $i$ to node $j$ is calculated using the following state transition rule:

$$p_{ij}^k = \frac{[\tau_{ij}]^\alpha [\eta_{ij}]^\beta}{\sum_{l \in N_i^k} [\tau_{il}]^\alpha [\eta_{il}]^\beta}$$

Where:
* $\tau_{ij}$ is the amount of pheromone on edge $i,j$.
* $\eta_{ij}$ is the desirability of the state transition (heuristic information, typically $1/d_{ij}$).
* $\alpha$ and $\beta$ are parameters controlling the influence of $\tau$ and $\eta$.

Pheromone evaporation is strictly controlled to avoid premature convergence:
$$\tau_{ij} \leftarrow (1 - \rho) \tau_{ij} + \Delta \tau_{ij}$$

### 2. 2-Opt Local Optimization
To resolve intersecting edges left by the stochastic nature of ACO, a 2-Opt mechanism is applied post-generation. It mathematically guarantees the removal of self-crossing paths in the graph, pushing the heuristic closer to the absolute global minimum without incurring an $O(n!)$ computational penalty.

## Copyright & Usage Rights
**© 2026 Assimous. All Rights Reserved.**

*This code is proprietary and provided for viewing purposes only to demonstrate algorithmic logic and research. You are NOT authorized to copy, modify, distribute, or use this software for any commercial or non-commercial purposes without explicit written permission.*

## Author
**Assimous** - *Lead Researcher & Developer*
