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
