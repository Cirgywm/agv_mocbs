# main_1.py

import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from CBS_1.grid import Grid
from CBS_1.heuristics import generate_heuristics
from CBS_1.mocbs import MOConflictBasedSearch

def draw_grid(grid, paths, starts, goals):
    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, grid.width - 0.5)
    ax.set_ylim(-0.5, grid.height - 0.5)
    ax.set_aspect('equal')
    ax.grid(True)

    # Draw obstacles
    for (x, y) in grid.obstacles:
        rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='black')
        ax.add_patch(rect)

    # Draw paths
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, (agent, (path, _)) in enumerate(paths.items()):
        color = colors[i % len(colors)]
        xs, ys = zip(*path)
        ax.plot(xs, ys, marker='o', label=f"Agent {agent}", color=color)

        # Start and goal
        ax.text(starts[agent][0], starts[agent][1], f"S{agent}", color='white', ha='center', va='center', bbox=dict(facecolor=color))
        ax.text(goals[agent][0], goals[agent][1], f"G{agent}", color='white', ha='center', va='center', bbox=dict(facecolor=color))

    ax.legend()
    plt.gca().invert_yaxis()
    plt.show()

def main():
    print("Program started", flush=True)
    width, height = 5, 5
    obstacles = set()
    grid = Grid(width, height, obstacles)

    starts = {
        'A': (0, 0),
        'B': (4, 4),
    }

    goals = {
        'A': (4, 0),
        'B': (0, 4),
    }

    heuristics = generate_heuristics(goals)
    planner = MOConflictBasedSearch(grid, starts, goals, heuristics)

    start_time = time.time()
    solution = planner.find_solution()
    elapsed_time = time.time() - start_time

    print(f"\nSolving Time: {elapsed_time:.4f} seconds\n")

    if solution:
        for agent, (path, cost) in solution.items():
            print(f"Agent {agent}:")
            print(f"  Path: {path}")
            print(f"  Cost: {cost}")
        draw_grid(grid, solution, starts, goals)
    else:
        print("No solution found.")

if __name__ == "__main__":
    print("start\n")
    main()
