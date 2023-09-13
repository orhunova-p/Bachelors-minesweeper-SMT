import pygame
from cell import Cell
from game import Game
from board import Board
size = (4, 4)
prob = 0.2
board = Board(size, prob)
# Sets the size of the screen
screen_size = (550, 550)
game = Game(board, screen_size)
game.run()

WIDTH = 30
HEIGHT = 30
# Sets the starting number of squares
NSQUARES = 10
# Sets the margin between each cell
MARGIN = 5
MENU_SIZE = 40
LEFT_CLICK = 1
RIGHT_CLICK = 3

#self.grid = [[self.Cell(x, y) for x in range(NSQUARES)] for y in range(NSQUARES)]