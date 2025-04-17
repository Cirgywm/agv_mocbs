# main.py

import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

from CBS_1.grid import Grid
from CBS_1.heuristics import generate_heuristics
from CBS_1.mocbs import MOConflictBasedSearch

def draw_static_grid(ax, grid, starts, goals):
    ax.set_xlim(-0.5, grid.width - 0.5)
    ax.set_ylim(-0.5, grid.height - 0.5)
    ax.set_aspect('equal')
    ax.set_xticks(range(grid.width))
    ax.set_yticks(range(grid.height))
    ax.grid(True)

    for (x, y) in grid.obstacles:
        rect = patches.Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='black')
        ax.add_patch(rect)

    for agent, pos in starts.items():
        ax.text(pos[0], pos[1], f"S{agent}", color='white', ha='center', va='center', bbox=dict(facecolor='blue'))
    for agent, pos in goals.items():
        ax.text(pos[0], pos[1], f"G{agent}", color='white', ha='center', va='center', bbox=dict(facecolor='green'))

def animate_paths(grid, paths, starts, goals):
    fig, ax = plt.subplots()
    draw_static_grid(ax, grid, starts, goals)

    agent_colors = ['blue', 'red', 'purple', 'orange', 'cyan']
    agents = list(paths.keys())
    max_steps = max(len(p[0]) for p in paths.values())

    circles = []
    for i, agent in enumerate(agents):
        x, y = paths[agent][0][0]  # initial pos
        circle = plt.Circle((x, y), 0.3, color=agent_colors[i % len(agent_colors)], label=f"Agent {agent}")
        ax.add_patch(circle)
        circles.append(circle)

    def update(frame):
        for i, agent in enumerate(agents):
            path = paths[agent][0]
            pos = path[min(frame, len(path)-1)]
            circles[i].center = pos
        return circles

    ani = animation.FuncAnimation(fig, update, frames=max_steps, interval=800, blit=True, repeat=False)
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()

def generate_random_map(width, height, num_obstacles, num_agents):
    all_cells = [(x, y) for x in range(width) for y in range(height)]
    obstacles = set(random.sample(all_cells, num_obstacles))

    empty_cells = [cell for cell in all_cells if cell not in obstacles]
    starts = {}
    goals = {}
    random.shuffle(empty_cells)
    for i in range(num_agents):
        starts[chr(65+i)] = empty_cells.pop()
        goals[chr(65+i)] = empty_cells.pop()

    return obstacles, starts, goals

def check_collisions(paths):
    max_steps = max(len(p[0]) for p in paths.values())
    collisions = {}

    for t in range(max_steps):
        positions = {}
        for agent, (path, _) in paths.items():
            pos = path[min(t, len(path)-1)]
            if pos in positions:
                if pos not in collisions:
                    collisions[pos] = []
                collisions[pos].append(agent)
                collisions[pos].append(positions[pos])
            else:
                positions[pos] = agent

    if collisions:
        print("\nCollisions detected:")
        for pos, agents in collisions.items():
            print(f"  At position {pos}: Agents {set(agents)}")
        print(f"Total collisions: {len(collisions)}\n")
    else:
        print("\nNo collisions detected.\n")

def main():
    print("Program started", flush=True)
    width, height = 8, 8
    num_obstacles = 10
    num_agents = 3

    obstacles, starts, goals = generate_random_map(width, height, num_obstacles, num_agents)
    grid = Grid(width, height, obstacles)

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
        check_collisions(solution)
        animate_paths(grid, solution, starts, goals)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
