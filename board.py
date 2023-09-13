import random
from itertools import product
from cell import Cell
from solver import SMT_Solver
class Board():
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.lost = False
        self.num_clicked = 0
        self.num_non_bombs = 0
        self.set_board()

    def reset(self):
        self.lost = False
        self.num_clicked = 0
        self.num_non_bombs = 0
        self.set_board()

    def set_board(self):
        #self.grid = [[self.Cell(x, y) for x in range(self.size[0])] for y in range(self.size[1])]
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                has_bomb = random.random() < self.prob
                if not has_bomb:
                    self.num_non_bombs += 1
                piece = Cell(has_bomb)
                row.append(piece)
            self.board.append(row)
        self.set_neighbours()
        #self.print_board()

    def print_board(self):
        print(self.board)
        print("shape", len(self.board), len(self.board[0]))
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.get_piece((row,col))
                if piece.has_bomb:
                    print("index:", row, col, "val", "*")
                else:
                    print("index:", row, col, "val", piece.get_num_around())

    def cheat(self):
        elements = list(range(len(self.board)))
        pairs = list(product(elements, repeat=2))
        random.shuffle(pairs)
        for q in range(9):
            for i, j in pairs:
                piece = self.board[i][j]
                #print("index:", i, j, "val=",  piece.get_num_around(), "i=", q)
                if piece.has_bomb == False and piece.clicked == False and piece.flagged == False and piece.get_num_around() == q:
                    self.handle_click(piece, False)
                    #print("result: found index:", i, j, "val=",  piece.get_num_around(), "i=", q)
                    return
                
    def solve(self):
        solver = SMT_Solver(self.board)
        safe_to_click, x, y = solver.solve()
        if safe_to_click:
            #print(safe_to_click, x, y)
            self.get_piece((x, y)).safe = True
            return True
        else:
            return False

    def set_neighbours(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.get_piece((row,col))
                neighbors = self.get_list_of_neighbors((row,col))
                piece.set_neighbors(neighbors)
    
    def get_list_of_neighbors(self, index):
        neighbors = []
        for row in range (index[0] - 1, index[0] + 2):
            for col in range (index[1] - 1, index[1] + 2):
                if row == index[0] and col == index[1]:
                    continue
                if row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]:
                    continue
                neighbors.append(self.get_piece((row, col)))
        return neighbors


    def get_size(self):
        return self.size
    
    def get_piece(self, index):
        return self.board[index[0]][index[1]]
        
    def handle_click(self, piece, flag):
        if piece.get_clicked() or (not flag and piece.get_flagged()):#if not False(rightclick)
            return
        elif flag:
            piece.toggle_flag()
            return
        piece.click()
        if piece.get_has_bomb():
            self.lost = True
            return
        self.num_clicked +=1
        if piece.get_num_around() != 0:
            return
        for neighbor in piece.get_neighbors():
            if not neighbor.get_has_bomb() and not neighbor.get_clicked():
                self.handle_click(neighbor, False)
        
    def get_won(self):
        return self.num_clicked == self.num_non_bombs
    
    def get_lost(self):
        return self.lost
