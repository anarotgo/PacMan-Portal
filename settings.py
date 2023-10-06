import pygame
import copy

from board import boards

pygame.init()

class Settings:
    def screen_dimensions():
        screen_width = 900
        screen_height = 950
        return screen_width, screen_height
    
    fps = 60
    font = pygame.font.Font('freesansbold.ttf', 20)
    level = copy.deepcopy(boards)
    color = 'blue'
    
    # locations and directions
    def pacman_loc_dir():
        pacman_x = 450
        pacman_y = 663
        pacman_direction = 0
        return pacman_x, pacman_y, pacman_direction
    def blinky_loc_dir():
        blinky_x = 56
        blinky_y = 58
        blinky_direction = 0
        return blinky_x, blinky_y, blinky_direction
    def inky_loc_dir():
        inky_x = 440
        inky_y = 388
        inky_direction = 2
        return inky_x, inky_y, inky_direction
    def pinky_loc_dir():    
        pinky_x = 440
        pinky_y = 438
        pinky_direction = 2
        return pinky_x, pinky_y, pinky_direction
    def clyde_loc_dir():
        clyde_x = 440
        clyde_y = 438
        clyde_direction = 2
        return clyde_x, clyde_y, clyde_direction