import pygame
import sys
import networkx as nx  # Import NetworkX for graph representation

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
    "######.# ######### #.######",
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
CELL_SIZE = 30  # Adjust as needed to fit your maze size
SCREEN_WIDTH = maze_width * CELL_SIZE
SCREEN_HEIGHT = maze_height * CELL_SIZE
pacman_speed = 1    # higher value == faster movement
frame_rate = 30

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Maze")

# Define colors
black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Define Pac-Man class
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # Adjust the radius as needed
        self.direction = "right"  # Pac-Man's initial direction
        self.color = (yellow)  # Yellow color

    def move(self):
        # Implement Pac-Man's movement logic here based on the direction
        if self.direction == "right":
            self.x += CELL_SIZE
        elif self.direction == "left":
            self.x -= CELL_SIZE
        elif self.direction == "up":
            self.y -= CELL_SIZE
        elif self.direction == "down":
            self.y += CELL_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Find a valid initial position for Pac-Man that is not a wall
pacman_initial_x = 0
pacman_initial_y = 0
for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char != "#":
            pacman_initial_x = x * CELL_SIZE + CELL_SIZE // 2
            pacman_initial_y = y * CELL_SIZE + CELL_SIZE // 2
            break
    if pacman_initial_x != 0:
        break

# Create Pac-Man instance
pacman = Pacman(pacman_initial_x, pacman_initial_y)  # Initial position of Pac-Man

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

# Game loop
running = True
moving = False  # Flag to track Pac-Man's movement
move_counter = 0

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
    if move_counter < pacman_speed:
        move_counter += 1
    else:
        # Reset move_counter
        move_counter = 0

        # Calculate Pac-Man's next position based on direction
        next_x, next_y = pacman.x, pacman.y
        if pacman.direction == "right":
            next_x += CELL_SIZE
        elif pacman.direction == "left":
            next_x -= CELL_SIZE
        elif pacman.direction == "up":
            next_y -= CELL_SIZE
        elif pacman.direction == "down":
            next_y += CELL_SIZE

        # Check if the next position is valid (not a wall)
        next_cell_x = next_x // CELL_SIZE
        next_cell_y = next_y // CELL_SIZE

        if (
            next_cell_x >= 0
            and next_cell_x < len(maze[0])
            and next_cell_y >= 0
            and next_cell_y < len(maze)
            and maze[next_cell_y][next_cell_x] not in ("#",)
        ):
            pacman.x = next_x
            pacman.y = next_y

        # Check if the next position is valid (not a wall) and within the graph
        if G.has_node((next_x // CELL_SIZE, next_y // CELL_SIZE)) and G.has_edge(
            (pacman.x // CELL_SIZE, pacman.y // CELL_SIZE), (next_x // CELL_SIZE, next_y // CELL_SIZE)
        ):
            # Move Pac-Man only when the arrow key is pressed
            if moving:
                pacman.x = next_x
                pacman.y = next_y

    # Clear the screen
    screen.fill(black)

    # Draw the maze, points, power pills, and Pac-Man
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, blue, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif char == ".":
                pygame.draw.circle(screen, yellow, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 2)
            elif char == "o":  # Represent power pills with asterisks
                pygame.draw.circle(screen, yellow, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 5)

    # Draw Pac-Man
    pacman.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(frame_rate)

# Quit Pygame
pygame.quit()
sys.exit()
