# mo_cbs/mocbs.py

import heapq
from CBS_1.mocbs_node import CBSNode, Constraint, Conflict

class MOConflictBasedSearch:
    def __init__(self, grid, starts, goals, heuristics):
        self.grid = grid
        self.starts = starts
        self.goals = goals
        self.heuristics = heuristics
        from CBS_1.namoa_star_optim import NAMOAStar
        self.low_level = NAMOAStar(grid, heuristics)

    def detect_conflict(self, paths):
        max_len = max(len(p[0]) for p in paths.values())
        for t in range(max_len):
            positions = {}
            for agent, (path, _) in paths.items():
                pos = path[min(t, len(path)-1)]
                if pos in positions:
                    return Conflict(agent, positions[pos], pos, t)
                positions[pos] = agent
        return None

    def create_constraints(self, conflict):
        return {
            Constraint(conflict.agent1, conflict.position, conflict.position),
            Constraint(conflict.agent2, conflict.position, conflict.position),
        }

    def find_solution(self):
        root_paths = {}
        for agent, start in self.starts.items():
            goal = self.goals[agent]
            print(f"Planning initial path for agent {agent}", flush=True)
            sols = self.low_level.search(agent, start, goal)
            if not sols:
                return None
            root_paths[agent] = sols[0]

        root = CBSNode(root_paths)
        open_list = [root]

        while open_list:
            open_list.sort()
            node = open_list.pop(0)
            print(f"Expanding CBS node with cost: {node.cost_vector} and {len(node.constraints)} constraints", flush=True)

            conflict = self.detect_conflict(node.paths)

            if not conflict:
                return node.paths

            for constraint in self.create_constraints(conflict):
                new_constraints = node.constraints | {constraint}
                new_paths = dict(node.paths)

                start = self.starts[constraint.agent]
                goal = self.goals[constraint.agent]
                valid_paths = self.low_level.search(constraint.agent, start, goal, {
                    (c.edge[0], c.edge[1]) for c in new_constraints if c.agent == constraint.agent
                })
                if not valid_paths:
                    continue

                new_paths[constraint.agent] = valid_paths[0]
                new_node = CBSNode(new_paths, new_constraints)
                heapq.heappush(open_list, new_node)

        return None
