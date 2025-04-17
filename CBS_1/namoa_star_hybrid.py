# mo_cbs/namoa_star.py

import heapq

class NAMOAStar:
    def __init__(self, grid, heuristics, epsilon=0.05, max_expansion=10000, max_solutions=3):
        self.grid = grid
        self.heuristics = heuristics
        self.epsilon = epsilon
        self.max_expansion = max_expansion
        self.max_solutions = max_solutions

    def approx_dominated(self, candidate, others):
        for other in others:
            if all(c <= (1 + self.epsilon) * o for c, o in zip(candidate, other)):
                return True
        return False

    def is_pareto_optimal(self, candidate, others):
        for other in others:
            if all(o <= c for o, c in zip(other, candidate)) and any(o < c for o, c in zip(other, candidate)):
                return False
        return True

    def search(self, agent, start, goal):
        open_list = []
        closed = []
        solutions = []

        h = self.heuristics[agent].get(start, [0, 0])
        start_node = (h, [0] * len(h), [start])
        heapq.heappush(open_list, start_node)

        expansions = 0

        while open_list and expansions < self.max_expansion:
            _, cost, path = heapq.heappop(open_list)
            current_pos = path[-1]

            expansions += 1

            if current_pos == goal:
                if self.is_pareto_optimal(cost, [c for _, c, _ in solutions]) and not self.approx_dominated(cost, [c for _, c, _ in solutions]):
                    solutions = [s for s in solutions if not self.approx_dominated(s[1], [cost])]
                    solutions.append((path, cost))
                if len(solutions) >= self.max_solutions:
                    break
                continue

            for neighbor in self.grid.get_neighbors(current_pos):
                if neighbor in path:
                    continue
                new_path = path + [neighbor]
                new_cost = [c + 1 for c in cost]
                h = self.heuristics[agent].get(neighbor, [0, 0])
                est_total = [c + h[i] for i, c in enumerate(new_cost)]

                if self.is_pareto_optimal(new_cost, [c for _, c, _ in open_list + closed]) and not self.approx_dominated(new_cost, [c for _, c, _ in open_list + closed]):
                    heapq.heappush(open_list, (est_total, new_cost, new_path))
            closed.append((_, cost, path))

        return solutions
