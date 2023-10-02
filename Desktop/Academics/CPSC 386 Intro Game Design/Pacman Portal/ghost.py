import pygame
from settings import Settings

# Define Ghost class
class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # Adjust the radius as needed
        self.direction = "right"  # Ghost's initial direction
        self.color = (255, 0, 0)  # Red color

    def move(self):
        # Implement ghost's automatic movement logic here (random direction)
        available_directions = []  # Store available directions to move

        # Check available directions (not hitting walls)
        next_x, next_y = self.x, self.y
        if self.direction == "right":
            next_x += Settings.cell_size
        elif self.direction == "left":
            next_x -= Settings.cell_size
        elif self.direction == "up":
            next_y -= Settings.cell_size
        elif self.direction == "down":
            next_y += Settings.cell_size

        next_cell_x = next_x // Settings.cell_size
        next_cell_y = next_y // Settings.cell_size

        # Check if next direction is valid
        if (
            next_cell_x >= 0
            and next_cell_x < len(maze[0])
            and next_cell_y >= 0
            and next_cell_y < len(maze)
            and maze[next_cell_y][next_cell_x] not in ("#",)
        ):
            available_directions.append(self.direction)

        # Randomly select a new direction from available directions
        new_direction = random.choice(available_directions)
        self.direction = new_direction

        # Update ghost's position based on the new direction
        if self.direction == "right":
            self.x += cell_size
        elif self.direction == "left":
            self.x -= cell_size
        elif self.direction == "up":
            self.y -= cell_size
        elif self.direction == "down":
            self.y += cell_size

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    