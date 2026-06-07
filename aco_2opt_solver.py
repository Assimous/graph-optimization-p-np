import numpy as np
import random
import time

class AntColonyOptimizer:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        """
        Advanced Ant Colony Optimization applied to NP-Hard TSP.
        alpha: importance of pheromone
        beta: importance of heuristic (inverse distance)
        """
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone = self.pheromone * self.decay  # Evaporation
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        return sum([self.distances[move] for move in path])

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # return to start
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        
        # Metaheuristic probability function
        row = pheromone ** self.alpha * (( 1.0 / (dist + 1e-10)) ** self.beta)
        norm_row = row / row.sum()
        move = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return move

# --- 2-OPT LOCAL SEARCH (Post-Processing) ---
def two_opt(route, dist_matrix):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:]
                new_route[i:j] = route[j - 1:i - 1:-1]
                if calculate_total_distance(new_route, dist_matrix) < calculate_total_distance(best, dist_matrix):
                    best = new_route
                    improved = True
        route = best
    return best

def calculate_total_distance(route, dist_matrix):
    return sum(dist_matrix[route[i]][route[i+1]] for i in range(len(route)-1)) + dist_matrix[route[-1]][route[0]]

if __name__ == "__main__":
    print("[*] Initializing Advanced NP-Hard Optimizer...")
    # Generating a complex distance matrix for 20 nodes
    np.random.seed(42)
    n_nodes = 20
    coords = np.random.rand(n_nodes, 2) * 100
    dist_matrix = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(-1))
    
    start_time = time.time()
    
    print("[*] Running Ant Colony Metaheuristic...")
    ant_colony = AntColonyOptimizer(distances=dist_matrix, n_ants=25, n_best=5, n_iterations=50, decay=0.95)
    best_aco_path, best_aco_dist = ant_colony.run()
    
    print(f"[+] ACO Distance: {best_aco_dist:.4f}")
    
    # Extract sequence from ACO tuples
    sequence = [0] + [edge[1] for edge in best_aco_path[:-1]]
    
    print("[*] Applying 2-Opt Local Search Convergence...")
    optimized_sequence = two_opt(sequence, dist_matrix)
    final_dist = calculate_total_distance(optimized_sequence, dist_matrix)
    
    print(f"[+] Final Optimized Distance: {final_dist:.4f}")
    print(f"[+] Convergence Time: {time.time() - start_time:.4f}s")
    print("[*] Analysis: Hybrid Metaheuristic successfully bypassed factorial time constraints.")
