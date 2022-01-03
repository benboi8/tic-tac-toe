import random

import pygame

pygame.init()  # Initialize pygame

# Screen
WIDTH = 900  # Screen width
HEIGHT = 900  # Screen height
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Screen


# background
def draw_background():  # Draw the board lines
    pygame.draw.line(screen, BLACK, (300, 0), (300, 900), 2)
    pygame.draw.line(screen, BLACK, (600, 0), (600, 900), 2)
    pygame.draw.line(screen, BLACK, (0, 300), (900, 300), 2)
    pygame.draw.line(screen, BLACK, (0, 600), (900, 600), 2)


# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# board pos
board_pos = [22, 322, 622]

# board values
board = [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "]]

# Moves done
moves = [[2, 2, 2],
         [2, 2, 2],
         [2, 2, 2]]

# Global variables
player_row = 0
player_col = 0
enemy_row = 0
enemy_col = 0
move_num = 0
weight = 0
running = True
pointerX = (WIDTH / 2) - 128
pointerY = (WIDTH / 2) - 128
p = 0
game_won = False

Ximg = pygame.image.load("X.png")
XposX = []
XposY = []

Oimg = pygame.image.load("O.png")
OposX = []
OposY = []


class PlayerMove:
    def validation(self):
        valid_move = False
        while not valid_move:
            if board[player_row][player_col] == " ":  # Check if board space is available
                valid_move = True
                self.placement(valid_move)  # Place X
            else:
                print("Invalid move")  # Inform user that move is invalid

    def placement(self, valid_move):
        if valid_move:
            board[player_row][player_col] = "X"  # Place in X
        else:
            self.validation()  # Catchment for false moves


class EnemyMove:
    def __init__(self, player_row, player_col):
        self.player_row = player_row  # Where the player moved, row
        self.player_col = player_col  # Where the player moved, col

    def validation(self, player_row, player_col):
        valid_move = False
        while not valid_move:
            # Choose a random number for enemy position
            enemy_row = random.randint(0, 2)
            enemy_col = random.randint(0, 2
                                       )

            if board[enemy_row][enemy_col] == " ":  # Check if move place is empty
                valid_move = True
                self.placement(valid_move, enemy_row, enemy_col)  # Draw O
            # Repeats if not empty

    def placement(self, valid, row, col):
        if valid:
            board[row][col] = "O"  # Place in O


class CalculateWinningMoves:
    def __init__(self, won, winning_counter="X"):
        self.won = won
        self.winning_counter = winning_counter  # Variable to check if X or O has won

    def row_calculations(self, winning_counter, won):
        # First row
        if moves[0][0] == winning_counter and moves[0][1] == winning_counter and moves[0][2] == winning_counter:
            won = True
        # Second row
        elif moves[1][0] == winning_counter and moves[1][1] == winning_counter and moves[1][2] == winning_counter:
            won = True
        # Third row
        elif moves[2][0] == winning_counter and moves[2][1] == winning_counter and moves[2][2] == winning_counter:
            won = True
        else:
            self.ChangeWinningCounter(winning_counter)

    def col_calulations(self, winning_counter, won):
        # First column
        if moves[0][0] == winning_counter and moves[1][0] == winning_counter and moves[2][0] == winning_counter:
            won = True
        # Second column
        elif moves[0][1] == winning_counter and moves[1][1] == winning_counter and moves[2][1] == winning_counter:
            won = True
        # Third column
        elif moves[0][2] == winning_counter and moves[1][2] == winning_counter and moves[2][2] == winning_counter:
            won = True
        else:
            self.ChangeWinningCounter(winning_counter)

    def diagonal_calculations(self, winning_counter, won):
        # Top left to bottom right
        if moves[0][0] == winning_counter and moves[1][1] == winning_counter and moves[2][2] == winning_counter:
            won = True
        # Top right to bottom left
        elif moves[2][0] == winning_counter and moves[1][1] == winning_counter and moves[0][2] == winning_counter:
            won = True
        else:
            self.ChangeWinningCounter(winning_counter)

    def ChangeWinningCounter(self, winning_counter):
        if winning_counter == "X":
            winning_counter = "O"
        else:
            winning_counter = "X"

    def CalculateWinner(self, won, is_player_turn):
        if won:
            if is_player_turn == "X":
                print("player won")  # Change these to on screen messages
            elif is_player_turn == "O":
                print("Player lost")  # Change these to on screen messages
        else:
            print("Tie")


class AddToList:
    def add_X_to_list(self, x, y):  # Add X move to list
        XposX.append(x)
        XposY.append(y)

    def add_O_to_list(self, x, y):  # Add O move to list
        OposX.append(x)
        OposY.append(y)


class Draw:
    def first_time_pointer(self):
        PointerImg = pygame.image.load("pointer.png")  # Load the image
        screen.blit(PointerImg, (pointerX, pointerY))

    def draw_pointer(self):
        for i in range(len(XposX)):
            if pointerX == XposX[i] and pointerY == XposY[i]:  # If X pointer overlaps with X
                PointerImg = pygame.image.load("X overlap.png")  # Load overlapping image
            elif pointerX == OposX[i] and pointerY == OposY[i]:  # if X pointer overlaps with O
                PointerImg = pygame.image.load("X overlap.png")  # Load overlapping image
        else:
            PointerImg = pygame.image.load("pointer.png")  # Draw normal pointer image

    def drawX(self):
        for i in range(len(XposX)):  # Go through all placed X's
            screen.blit(Ximg, (XposX[i], XposY[i]))  # Draw placed X

    def drawO(self):
        for i in range(len(OposX)):  # Go through all placed O's
            screen.blit(Oimg, (OposX[i], OposY[i]))  # Draw placed O


# Main Game loop
while running:
    # RGB values for background
    screen.fill(WHITE)
    draw_background()

    # Checks every event
    for event in pygame.event.get():
        # Check if event is quiting
        if event.type == pygame.QUIT:
            # Ends loop
            running = False

        # if keystroke is pressed check if it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not pointerX - 300 <= 0:
                    pointerX -= 300
            if event.key == pygame.K_RIGHT:
                if not pointerX + 300 >= WIDTH - 128:
                    pointerX += 300
            if event.key == pygame.K_UP:
                if not pointerY - 300 <= 0:
                    pointerY -= 300
            if event.key == pygame.K_DOWN:
                if not pointerY + 300 >= HEIGHT - 128:
                    pointerY += 300
            if event.key == pygame.K_RETURN:
                AddToList.add_X_to_list(AddToList, pointerX, pointerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                EnemyMove.validation(EnemyMove, player_row, player_col)
