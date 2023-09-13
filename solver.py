import random
from z3 import *
import time

class SMT_Solver():
    def __init__(self, board):
        self.board = board

    def solve(self):
        """call the function that sreate borders first, 
        than assign acceptable values to the closed cells
        and assign 0 values for the opened cells (in the cell class).
        Build and solve the expression.
        """

        self.create_borders()
        s = SimpleSolver()
        variables = {}
        for row in range(len(self.n_board)):
            for col in range(len(self.n_board[0])):
                variables[row, col] = Int("r%d_c%d" %(row, col))
                if self.n_board[row][col] == -1:
                    #denotes valid values (0 or 1) for closed cells
                    s.add(Or(variables[(row, col)] == 0, variables[(row, col)] == 1))
                else:
                    s.add(variables[(row, col)] == 0)
        for row in range(1, len(self.board)+1):
            for col in range(1, len(self.board[0])+1):
                if self.board[row - 1][col - 1].clicked:
                    expression = self.expression(variables, row, col)
                    s.add(expression)


        for i in self.choose_random_cell():
            s_new = s.__copy__()
            x, y = i
            s_new.add(variables[(x+1, y+1)] == 1)    
            result = s_new.check()
            if result == unsat:
                break
        if result == unsat:
            return True, x, y #safe to ckick
        else:
            return False, x, y #no safe


    def create_board(self):
        #Сreate table of tuples for each cell where first element in tuple 
        # represents number (from 0 to 8) of bombs around clicked cells 
        # or "-1" if the cell is not clicked
        self.n_board = [[0 for _ in range(len(self.board))] for _ in range(len(self.board[0]))]
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                num = -1
                if piece.clicked:
                    num = piece.label
                self.n_board[row][col] = num

    def create_borders(self):
        #return board with borders
        self.create_board()
        piece = 0
        new_row = []
        len_row = (len(self.n_board[0]))
        for row in self.n_board:
            row.append(piece)
            row.insert(0, piece)
        for i in range(len_row + 2):
            new_row.append(piece)
        self.n_board.append(new_row)
        self.n_board.insert(0, new_row)      

    def choose_random_cell(self):
        #creates a list to check for a random cell
        random_list = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                if not piece.clicked:
                    random_list.append((row,col))
        random.shuffle(random_list)
        #print(random_list)
        return random_list
    
    def expression(self, variables, row, col):
        expression = variables[(row - 1, col + 1)] + variables[(row, col + 1)] + \
        variables[(row + 1, col + 1)] + variables[(row + 1, col)] + \
        variables[(row + 1, col - 1)] + variables[(row, col - 1)] + \
        variables[(row - 1, col - 1)] + variables[(row - 1, col)] == int(self.n_board[row][col])
        return expression
