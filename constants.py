import pygame

pygame.init()

# Main window size

CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# Map
MAP_WIDTH = 40
MAP_HEIGHT = 40
MAP_MAX_ROOMS = 10

ROOM_MAX_HEIGHT = 7
ROOM_MAX_WIDTH = 5
ROOM_MIN_HEIGHT = 3
ROOM_MIN_WIDTH = 3

# FOV
TORCH_RAD= 8
FOV_LIGHT_WALLS = True
FOV_ALGO = 0

MESSAGE_LOG_NUM = 4
MAX_FPS = 60

# Colour
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_LIME = (50, 205, 50)
COLOR_YELLOW = (255,255,0)

# FONT
FONT_DEBUG = pygame.font.Font("data/JOYSTIX.TTF", 16)
FONT_MESSAGE = pygame.font.Font("data/JOYSTIX.TTF", 12)
FONT_CURSOR_TEXT = pygame.font.Font("data/JOYSTIX.TTF", CELL_HEIGHT)

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

# Draw Depth
DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100
DEPTH_BKGD = 150