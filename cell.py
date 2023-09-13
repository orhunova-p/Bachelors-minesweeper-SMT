class Cell:
    def __init__(self, has_bomb):
        self.has_bomb = has_bomb
        self.clicked = False
        self.flagged = False
        self.label = 0
        self.safe = False

    def safe_to_click(self):
        return self.safe
    
    def get_has_bomb(self):
        return self.has_bomb
    
    def get_clicked(self):
        return self.clicked
    
    def get_flagged(self):
        return self.flagged

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.set_num_bobms_around()
    
    def get_neighbors(self):
        return self.neighbors

    def set_num_bobms_around(self):
        self.label = 0
        for piece in self.neighbors:
            if (piece.get_has_bomb()):
               self.label +=1 
    
    def get_num_around(self):
        return self.label
    
    def toggle_flag(self):
        self.flagged = not self.flagged

    def click(self):
        self.clicked = True
