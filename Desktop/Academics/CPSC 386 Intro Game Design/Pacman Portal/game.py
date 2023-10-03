import pygame
import sys
import networkx as nx  # Import NetworkX for graph representation
import random
from pacman import Pacman
from ghost import Ghost
from settings import Settings
from mazes import maze_list

def draw_maze():
    # Draw the maze, points, power pills, and Pac-Man
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "#":
                pygame.draw.rect(screen, Settings.blue, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif char == ".":
                pygame.draw.circle(screen, Settings.yellow, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 2)
            elif char == "o":  # Represent power pills with asterisks
                pygame.draw.circle(screen, Settings.yellow, (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 5)
            elif char == "_":    # Draw the gate for ghosts
                pygame.draw.rect(screen, Settings.blue, (x * cell_size, y * cell_size, cell_size, cell_size/2))
def display_score():
     # Display the score, powered up status, and ghosts eaten
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, Settings.white)
    status_text = font.render("Powered up" if powered_up else "Default", True, Settings.white)
    ghosts_text = font.render(f"Ghosts eaten: {ghosts_eaten}", True, Settings.white)
    
    score_rect = score_text.get_rect(topleft=(SCREEN_WIDTH - 120, 10))
    status_rect = status_text.get_rect(topleft=(SCREEN_WIDTH - 120, 40))  # Adjust the vertical position
    ghosts_rect = ghosts_text.get_rect(topleft=(SCREEN_WIDTH - 120, 70))  # Adjust the vertical position
    
    screen.blit(score_text, score_rect)
    screen.blit(status_text, status_rect)
    screen.blit(ghosts_text, ghosts_rect)


# Define the Pac-Man maze as a 2D grid
maze = maze_list[1] # Gets a certain maze design from mazes.py

# Initialize Pygame
pygame.init()

# Define constants
maze_width = len(maze[0])
maze_height = len(maze)
cell_size = Settings.cell_size
# Screen size
SCREEN_WIDTH = maze_width * cell_size; SCREEN_HEIGHT = maze_height * cell_size
# Speeds
pacman_speed = 1
frame_rate = 30
ghost_speed = 1

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Track points
points_collected = 0; power_pills_collected = 0; ghosts_eaten = 0

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Portal")

# Find a valid initial position for Pac-Man that is not a wall
pacman_initial_x = 0; pacman_initial_y = 0
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
ghost_initial_x = 0; ghost_initial_y = 0
for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "x":
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

# Game loop variables
running = True
moving = False  # Flag to track Pac-Man's movement
pacman_move_counter = 0
score = 0
powered_up = False

ghost_move_counter = 0

game_over = False
try_again_clicked = False

try_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)

# Game loop ****************************************************
while running:
    try_again_clicked = False
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for keydown and keyup events
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
        # Check for try again button click
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Check if the mouse click is inside the "Try Again" button
            if try_again_button_rect.collidepoint(event.pos):
                # Reset the game
                game_over = False
                try_again_clicked = True
                pacman.x, pacman.y = pacman_initial_x, pacman_initial_y
                ghost.x, ghost.y = ghost_initial_x, ghost_initial_y

    # Move Pac-Man gradually based on the move_counter
    if not game_over and not try_again_clicked:
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
                    score += 10
                    # Remove the point from the maze
                    maze[next_cell_y] = maze[next_cell_y][:next_cell_x] + " " + maze[next_cell_y][next_cell_x + 1:]

                # Check if Pac-Man has eaten a power pill
                elif maze[next_cell_y][next_cell_x] == "o":
                    power_pills_collected += 1
                    powered_up = True
                    score += 50
                    # Remove the power pill from the maze
                    maze[next_cell_y] = maze[next_cell_y][:next_cell_x] + " " + maze[next_cell_y][next_cell_x + 1:]

                # Check if Pac-Man collided with the ghost
                if pygame.Rect(pacman.x - pacman.radius, pacman.y - pacman.radius, 2 * pacman.radius, 2 * pacman.radius).colliderect(
                    pygame.Rect(ghost.x - ghost.radius, ghost.y - ghost.radius, 2 * ghost.radius, 2 * ghost.radius)
                ):
                    if powered_up:
                        # Eat the ghost
                        ghosts_eaten += 1
                        # Find the ghost's position in the maze and remove it
                        ghost_cell_x = int(ghost.x // cell_size)
                        ghost_cell_y = int(ghost.y // cell_size)
                        if 0 <= ghost_cell_x < len(maze[0]) and 0 <= ghost_cell_y < len(maze):
                            maze[ghost_cell_y] = maze[ghost_cell_y][:ghost_cell_x] + " " + maze[ghost_cell_y][ghost_cell_x + 1:]
                        # Add score
                        score += ghosts_eaten * 400
                    elif not powered_up:
                        game_over = True  # Set game over flag to True

        # *** Need to fix the ghost not moving on its own***
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
    screen.fill(Settings.black)
    
    draw_maze()
    
    # Draw Pac-Man and ghost
    pacman.draw(screen)
    ghost.draw(screen)

    # Draw game-over message if game is over
    if game_over:
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over", True, Settings.red)
        try_again_text = font.render("Try Again", True, Settings.red)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - cell_size))
        try_again_rect = try_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + cell_size))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(try_again_text, try_again_rect)
    
    display_score()

    # Update the display
    pygame.display.flip()
    # Control the frame rate
    clock.tick(frame_rate)

# Quit Pygame
pygame.quit()
sys.exit()