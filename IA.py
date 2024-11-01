import pygame
import numpy as np
from collections import deque

# Constants
CELL_SIZE = 100
GRID_SIZE = (5, 5)
OBSTACLES = [(1, 1), (1, 2), (2, 1)]
TARGET = (4, 4)
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class GridWorld:
    def __init__(self, size, obstacles, target):
        self.size = size
        self.grid = np.zeros(size)
        self.obstacles = obstacles
        self.target = target
        self.place_obstacles()

    def place_obstacles(self):
        for obs in self.obstacles:
            self.grid[obs] = -1  # -1 represents an obstacle

    def is_valid_move(self, position):
        x, y = position
        if (0 <= x < self.size[0]) and (0 <= y < self.size[1]):
            return self.grid[x, y] != -1  # Check for obstacles
        return False

class Agent:
    def __init__(self, position):
        self.position = position

    def sense(self, grid_world):
        x, y = self.position
        surroundings = {
            'up': grid_world.is_valid_move((x-1, y)),
            'down': grid_world.is_valid_move((x+1, y)),
            'left': grid_world.is_valid_move((x, y-1)),
            'right': grid_world.is_valid_move((x, y+1)),
        }
        return surroundings

    def move(self, direction):
        if direction == 'up':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'down':
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == 'left':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'right':
            self.position = (self.position[0], self.position[1] + 1)

def bfs(grid_world, start, target):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == target:
            break

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if grid_world.is_valid_move(neighbor) and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current

    return parent

def reconstruct_path(parent, start, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    path.reverse()
    return path

def draw_grid(screen, grid_world, agent_position):
    for x in range(grid_world.size[0]):
        for y in range(grid_world.size[1]):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) in grid_world.obstacles:
                pygame.draw.rect(screen, BLACK, rect)
            elif (x, y) == grid_world.target:
                pygame.draw.rect(screen, GREEN, rect)
            elif (x, y) == agent_position:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Grid lines

def main():
    pygame.init()
    screen = pygame.display.set_mode((CELL_SIZE * GRID_SIZE[1], CELL_SIZE * GRID_SIZE[0]))
    clock = pygame.time.Clock()

    grid_world = GridWorld(GRID_SIZE, OBSTACLES, TARGET)
    agent = Agent((0, 0))

    path = bfs(grid_world, agent.position, grid_world.target)
    target_path = reconstruct_path(path, agent.position, grid_world.target)

    running = True
    step_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_grid(screen, grid_world, agent.position)

        if step_index < len(target_path):
            next_position = target_path[step_index]
            agent.move('down' if next_position[0] > agent.position[0] else 'up' if next_position[0] < agent.position[0] else 'right' if next_position[1] > agent.position[1] else 'left')
            step_index += 1

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()