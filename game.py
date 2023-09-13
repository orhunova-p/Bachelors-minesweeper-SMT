import pygame
import math
from time import sleep

class Game():
    def __init__(self, board, screen_size):
        self.board = board
        self.screen_size = screen_size
        self.piece_size = (self.screen_size[0] - 120 - 30) / self.board.get_size()[1], (self.screen_size[1] - 120 - 30) / self.board.get_size()[0]
    
    def run(self):
        pygame.init
        #set the size of window
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Minesweeper') 
        background_colour = (190, 190, 190, 255)
        #function that draw the buttons  
        self.screen.fill(background_colour)
        #closing the window
        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    position = pygame.mouse.get_pos()
                    right_click = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handle_clik(position, right_click)
            self.draw_board() #function that draw the board
            self.draw_buttons()
            pygame.display.flip()
            if self.board.get_won():
                #print("You won!")
                pygame.mixer.init()
                sound = pygame.mixer.Sound("win.wav")
                sound.play()
                sleep(3)
                running = False
        pygame.QUIT

    def solution_not_found(self):
        running_text = True
        while running_text:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.QUIT
                    quit()
            font = pygame.font.SysFont("twsenmt", 50)
            self.draw_text("Solution is not found", font, (36, 36, 36), 250, 310, ((0, 255, 255)))
            pygame.display.flip()
            sleep(2)
            running_text = False
        self.screen.fill((190, 190, 190, 255))  #Restore the original background color
        pygame.display.flip()

    def draw_board(self):
        top_left = (50, 110)
        for row in range (self.board.get_size()[0]):
            for col in range (self.board.get_size()[1]):
                piece = self.board.get_piece((row, col))
                cell_rect = pygame.Rect(top_left[0], top_left[1], self.piece_size[0] - 1, self.piece_size[0] - 1)
                cell_color = self.get_color(piece)
                pygame.draw.rect(self.screen, cell_color, cell_rect)

                self.set_numbers(piece, cell_rect)

                """num_bombs = piece.get_num_around()
                if num_bombs !=0:  # Exclude cells with 0 bombs around
                    pygame.font.init()
                    font = pygame.font.SysFont("Arial", 10)
                    text_surface = font.render(str(num_bombs), True, (0, 0, 255))
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    self.screen.blit(text_surface, text_rect)"""
                

                top_left = top_left[0] + self.piece_size[0], top_left[1]
            top_left = 50, top_left[1] + self.piece_size[1]

    def button_click(self, button_number):
        # Implement the functionality for each button
        if button_number == 1:
            flag = self.board.solve()
            if not flag:
                #print("NOT FOUND")
                self.solution_not_found()
            #print("Button 1 clicked!")
        elif button_number == 2:
            self.board.reset()
            #print("Button 2 clicked!")
        elif button_number == 3:
            self.board.cheat()
            #print("Button 3 clicked!")
        
    def draw_buttons(self):
        button1_rect = pygame.Rect(50, 40, 100, 40) #(left, top, width, height) sum_height = 80
        button2_rect = pygame.Rect(200, 40, 100, 40)
        #button3_rect = pygame.Rect(350, 40, 100, 40)

        button3_radius = 20  # Radius of the circle button
        button3_center = (385, 60)

        pygame.draw.rect(self.screen, (160, 32, 240, 255), button1_rect)
        pygame.draw.rect(self.screen, (160, 32, 240, 255), button2_rect)
        pygame.draw.circle(self.screen, (0, 255, 255, 255), button3_center, button3_radius)

        pygame.font.init()
        font = pygame.font.SysFont("twsenmt", 24)

        text1 = font.render("Solve step", True, (255, 255, 255))
        text2 = font.render("New game", True, (255, 255, 255))
        text3 = font.render("here", True, (36, 36, 36))

        # Calculate the center position of each button
        button1_text_pos = (
            button1_rect.centerx - text1.get_width() // 2,
            button1_rect.centery - text1.get_height() // 2
        )
        button2_text_pos = (
            button2_rect.centerx - text2.get_width() // 2,
            button2_rect.centery - text2.get_height() // 2
        )
        button3_text_pos = (
            button3_center[0] - text3.get_width() // 2,
            button3_center[1] - text3.get_height() // 2
        )

        self.screen.blit(text1, button1_text_pos)
        self.screen.blit(text2, button2_text_pos)
        self.screen.blit(text3, button3_text_pos)

        self.draw_text("Click", font, (36, 36, 36), 342, 60)
        self.draw_text("to: a) cheat -.-", font, (36, 36, 36), 460, 60)
        self.draw_text("b) safe start", font, (36, 36, 36), 478, 80)
    
    def draw_text(self, text, font, text_col, x, y, rect_col=(190, 190, 190, 255)):
        text = font.render(text, True, text_col, rect_col)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)

    def get_color(self, piece):
        color = ()
        if piece.get_clicked():
            if piece.get_has_bomb():
                color = (255, 0, 0) #bomb
            elif piece.get_has_bomb() == False:
                color = (255, 255, 255) #empty with number
        elif piece.get_flagged():
            color = (255, 110, 180) #flag
        elif piece.safe_to_click():
            color = (127, 255, 212) #solved with solver 
        else:
            color = (255, 255, 0) #not yet clicked
        return color

    def set_numbers(self, piece, cell_rect):
        num_bombs = piece.get_num_around()
        if piece.get_clicked() and piece.get_has_bomb() == False and  num_bombs !=0:  # Exclude cells with 0 bombs around
            pygame.font.init()
            font = pygame.font.SysFont("Arial", 10)
            text_surface = font.render(str(num_bombs), True, (0, 0, 255))
            text_rect = text_surface.get_rect(center=cell_rect.center)
            self.screen.blit(text_surface, text_rect)

    def is_point_inside_circle(self, position, center, radius):
        # Calculate the distance between the point and the center of the circle
        distance = math.sqrt((position[0] - center[0])**2 + (position[1] - center[1])**2)
        return distance <= radius

    def handle_clik(self, position, right_click):
        if self.board.get_lost():
            if position[0] > 200 and position[0] < 300 and position[1] > 40 and position[1] < 80:
                self.button_click(2)
        else:
            if position[0] > 50 and position[0] < 150 and position[1] > 40 and position[1] < 80:
                self.button_click(1)
            elif position[0] > 200 and position[0] < 300 and position[1] > 40 and position[1] < 80:
                self.button_click(2)
            elif position[0] > 50 and position[0] < 500 and position[1] > 110 and position[1] < 510:
                index = int((position[1] - 110) // self.piece_size[1]), int((position[0] - 50) // self.piece_size[1])
                piece = self.board.get_piece(index)
                self.board.handle_click(piece, right_click)
            elif self.is_point_inside_circle(position, (385, 60), 20):
                self.button_click(3)





