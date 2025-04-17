# mo_cbs/grid.py

class Grid:
    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos):
        return pos not in self.obstacles

    def get_neighbors(self, pos):
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = [(x + dx, y + dy) for dx, dy in directions]
        # print(f"Checking neighbors for {pos}: {[n for n in neighbors if self.in_bounds(n)]}")
        return [p for p in neighbors if self.in_bounds(p) and self.passable(p)]

    def get_cost(self, from_node, to_node):
        # Example with 2 objectives: (distance, time)
        return (1, 1)  # uniform cost for simplicity
