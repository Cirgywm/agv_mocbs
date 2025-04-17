# mo_cbs/namoa_star_optim.py

import heapq

class NAMOAStar:
    def __init__(self, grid, heuristics):
        self.grid = grid
        self.heuristics = heuristics  # {agent_id: {(x, y): (h1, h2, ...)}}

    def dominates(self, a, b):
        return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))

    def is_pareto_optimal(self, frontier, new_cost):
        non_dominated = []
        dominated = False
        for cost in frontier:
            if self.dominates(cost, new_cost):
                dominated = True
                break
            if not self.dominates(new_cost, cost):
                non_dominated.append(cost)
        if not dominated:
            non_dominated.append(new_cost)
        return non_dominated, not dominated

    def search(self, agent_id, start, goal, constraints=None):
        print(f"[{agent_id}] NAMOA* starting from {start} to {goal}", flush=True)
        open_set = []
        heapq.heappush(open_set, (self.heuristics[agent_id][start], start, []))  # (cost, pos, path)
        visited = {}

        solutions = []

        max_expansions = 10000
        expansions = 0

        while open_set and expansions < max_expansions:
            expansions += 1

            cost, pos, path = heapq.heappop(open_set)

            if pos == goal:
                solutions.append((path + [pos], cost))
                continue

            for neighbor in self.grid.get_neighbors(pos):
                if constraints and (pos, neighbor) in constraints:
                    continue

                step_cost = self.grid.get_cost(pos, neighbor)
                new_cost = tuple(c + s for c, s in zip(cost, step_cost))
                heuristic = self.heuristics[agent_id].get(neighbor, (0, 0))
                total_estimated = tuple(c + h for c, h in zip(new_cost, heuristic))

                state = (neighbor, len(path) + 1)
                if state not in visited or self.dominates(new_cost, visited[state]):
                    visited[state] = new_cost
                    heapq.heappush(open_set, (new_cost, neighbor, path + [pos]))

        print(f"[{agent_id}] Reached expansion limit!", flush=True)

        return solutions
