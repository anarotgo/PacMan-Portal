import pygame
import sys
import networkx as nx  # Import NetworkX for graph representation
import random
from pacman import Pacman
from ghost import Ghost
from settings import Settings

# Define the Pac-Man maze as a 2D grid
maze = [
    "###########################",
    "#............#............#",
    "#o####.#####.#.#####.####o#",
    "#.####.#####.#.#####.####.#",
    "#.........................#",
    "#.####.#.#########.#.####.#",
    "#......#.....#.....#......#",
    "######.##### # #####.######",
    "     #.#           #.#     ",
    "######.# ####_#### #.######",
    "         #       #         ",
    "######.# ######### #.######",
    "     #.#           #.#     ",
    "######.##### # #####.######",
    "#o.....#.....#.....#.....o#",
    "#.####.#.#########.#.####.#",
    "#.........................#",
    "#.####.#####.#.#####.####.#",
    "#.####.#####.#.#####.####.#",
    "#............#............#",
    "###########################"
]

# Initialize Pygame
pygame.init()

# Define constants
maze_width = len(maze[0])
maze_height = len(maze)
cell_size = Settings.cell_size
# Colors
yellow = Settings.yellow
black = Settings.black
blue = Settings.blue
# Screen size
SCREEN_WIDTH = maze_width * cell_size
SCREEN_HEIGHT = maze_height * cell_size
# Speeds
pacman_speed = 1    # higher value == faster movement
frame_rate = 30
ghost_speed = 1

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Track points
points_collected = 0
power_pills_collected = 0

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Maze")

# Find a valid initial position for Pac-Man that is not a wall
pacman_initial_x = 0
pacman_initial_y = 0
for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char != "#":
            pacman_initial_x = x * cell_size + cell_size // 2
            pacman_initial_y = y * cell_size + cell_size // 2
            break
    if pacman_initial_x != 0:
        break
# Create Pac-Man instance
pacman = Pacman(pacman_initial_x, pacman_initial_y)  # Initial position of Pac-Man

# Find a valid initial position for ghost that is not a wall
ghost_initial_x = 0
ghost_initial_y = 0
for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char != "#":
            ghost_initial_x = x * cell_size + cell_size // 2
            ghost_initial_y = y * cell_size + cell_size // 2
            break
    if ghost_initial_x != 0:
        break
# Create Ghost instance with an initial position
ghost = Ghost(ghost_initial_x, ghost_initial_y)

# Create a graph to represent the maze
G = nx.Graph()
for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char != "#":
            G.add_node((x, y))
            if x > 0 and maze[y][x - 1] != "#":
                G.add_edge((x, y), (x - 1, y))
            if x < len(maze[y]) - 1 and maze[y][x + 1] != "#":
                G.add_edge((x, y), (x + 1, y))
            if y > 0 and maze[y - 1][x] != "#":
                G.add_edge((x, y), (x, y - 1))
            if y < len(maze) - 1 and maze[y + 1][x] != "#":
                G.add_edge((x, y), (x, y + 1))


running = True
moving = False  # Flag to track Pac-Man's movement
pacman_move_counter = 0
ghost_move_counter = 0
# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Handle Pac-Man's direction based on arrow key inputs
            if event.key == pygame.K_RIGHT:
                pacman.direction = "right"
                moving = True
            elif event.key == pygame.K_LEFT:
                pacman.direction = "left"
                moving = True
            elif event.key == pygame.K_UP:
                pacman.direction = "up"
                moving = True
            elif event.key == pygame.K_DOWN:
                pacman.direction = "down"
                moving = True
        elif event.type == pygame.KEYUP:
            # Stop Pac-Man's movement when the key is released
            moving = False

    # Move Pac-Man gradually based on the move_counter
    if pacman_move_counter < pacman_speed:
        pacman_move_counter += 1
    else:
        # Reset move_counter
        pacman_move_counter = 0

        # Calculate Pac-Man's next position based on direction
        next_x, next_y = pacman.x, pacman.y
        if pacman.direction == "right":
            next_x += cell_size
        elif pacman.direction == "left":
            next_x -= cell_size
        elif pacman.direction == "up":
            next_y -= cell_size
        elif pacman.direction == "down":
            next_y += cell_size

        # Check if the next position is valid (not a wall)
        next_cell_x = next_x // cell_size
        next_cell_y = next_y // cell_size

        if (
            next_cell_x >= 0
            and next_cell_x < len(maze[0])
            and next_cell_y >= 0
            and next_cell_y < len(maze)
            and maze[next_cell_y][next_cell_x] not in ("#",)
        ):
            pacman.x = next_x
            pacman.y = next_y

            # Check if Pac-Man has eaten a point
            if maze[next_cell_y][next_cell_x] == ".":
                points_collected += 1
                # Remove the point from the maze
                maze[next_cell_y] = maze[next_cell_y][:next_cell_x] + " " + maze[next_cell_y][next_cell_x + 1:]

            # Check if Pac-Man has eaten a power pill
            elif maze[next_cell_y][next_cell_x] == "o":
                power_pills_collected += 1
                # Remove the power pill from the maze
                maze[next_cell_y] = maze[next_cell_y][:next_cell_x] + " " + maze[next_cell_y][next_cell_x + 1:]

        # Check if the next position is valid (not a wall) and within the graph
        if G.has_node((next_x // cell_size, next_y // cell_size)) and G.has_edge(
            (pacman.x // cell_size, pacman.y // cell_size), (next_x // cell_size, next_y // cell_size)
        ):
            # Move Pac-Man only when the arrow key is pressed
            if moving:
                pacman.x = next_x
                pacman.y = next_y

    # Move Ghost gradually based on the move_counter
    if ghost_move_counter < ghost_speed:
        ghost_move_counter += 1
    else:
        # Reset move_counter
        ghost_move_counter = 0

        # Calculate Ghost's next position based on direction
        next_x, next_y = ghost.x, ghost.y
        # Implement ghost's movement logic here (e.g., random movement)

        # Check if the next position is valid (not a wall)
        next_cell_x = next_x // cell_size
        next_cell_y = next_y // cell_size

        if (
            next_cell_x >= 0
            and next_cell_x < len(maze[0])
            and next_cell_y >= 0
            and next_cell_y < len(maze)
            and maze[next_cell_y][next_cell_x] not in ("#",)
        ):
            ghost.x = next_x
            ghost.y = next_y

    # Clear the screen
    screen.fill(black)

    # Draw the maze, points, power pills, and Pac-Man
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, blue, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif char == ".":
                pygame.draw.circle(screen, yellow, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 2)
            elif char == "o":  # Represent power pills with asterisks
                pygame.draw.circle(screen, yellow, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 5)
            elif char == "_":    # Draw the gate for ghosts
                pygame.draw.rect(screen, blue, (x * cell_size, y * cell_size, cell_size, cell_size/2))
    
    # Draw Pac-Man and ghost
    pacman.draw(screen)
    ghost.draw(screen)
    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(frame_rate)

# Quit Pygame
pygame.quit()
sys.exit()
