# mo_cbs/heuristics.py

def manhattan_heuristic(goal):
    """Returns a heuristic function based on Manhattan distance."""
    def h(pos):
        dx = abs(goal[0] - pos[0])
        dy = abs(goal[1] - pos[1])
        return (dx, dy)  # Heuristic for (distance, time)
    return h

def generate_heuristics(goals):
    """Generate a dict of consistent heuristics per agent."""
    heuristics = {}
    for agent_id, goal in goals.items():
        heuristics[agent_id] = {}
        h_func = manhattan_heuristic(goal)
        for x in range(100):  # Adjust grid size as needed
            for y in range(100):
                heuristics[agent_id][(x, y)] = h_func((x, y))
    return heuristics
