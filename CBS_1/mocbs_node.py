# mo_cbs/mocbs_node.py

class Constraint:
    def __init__(self, agent, from_pos, to_pos):
        self.agent = agent
        self.edge = (from_pos, to_pos)

    def __eq__(self, other):
        return self.agent == other.agent and self.edge == other.edge

    def __hash__(self):
        return hash((self.agent, self.edge))

class Conflict:
    def __init__(self, agent1, agent2, position, timestep):
        self.agent1 = agent1
        self.agent2 = agent2
        self.position = position
        self.timestep = timestep

class CBSNode:
    def __init__(self, paths, constraints=None):
        self.paths = paths  # {agent_id: (path, cost)}
        self.constraints = constraints if constraints else set()
        self.cost_vector = self.compute_cost_vector()

    def compute_cost_vector(self):
        # Combine all costs lexicographically
        total = [0] * len(next(iter(self.paths.values()))[1])
        for path, cost in self.paths.values():
            total = [sum(x) for x in zip(total, cost)]
        return tuple(total)

    def __lt__(self, other):
        return self.cost_vector < other.cost_vector
