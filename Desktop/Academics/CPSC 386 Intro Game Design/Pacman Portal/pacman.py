import pygame
from settings import Settings

yellow = (255, 255, 0)
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
            self.x += Settings.cell_size
        elif self.direction == "left":
            self.x -= Settings.cell_size
        elif self.direction == "up":
            self.y -= Settings.cell_size
        elif self.direction == "down":
            self.y += Settings.cell_size

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)