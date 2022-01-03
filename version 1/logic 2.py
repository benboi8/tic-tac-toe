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
row = 0
col = 0
crow = 0
ccol = 0
move_num = 0
weight = 0
running = True
pointerX = (WIDTH / 2) - 128
pointerY = (WIDTH / 2) - 128
p = 0


def player_move():
    valid_move = False
    while not valid_move:
        """Put in pos of cursor controlled by arrow keys"""
        if board[row][col] == " ":  # Check if board space is available
            board[row][col] = "X"  # Place in X
            valid_move = True
            # all_moves(row, col, True)
        else:
            print("Invalid move")
    enemy_move(row, col)
    return row, col


def enemy_move(p_row, p_col):
    global weight, p, crow, ccol
    if (p_row != 1 and p_col != 1) and board[0][0] == " ":  # Top Left
        weight = 0
        p = 1
    elif (p_row != 1 and p_col != 1) and board[0][1] == " ":  # Top Middle
        weight = 1
        p = 2
    elif (p_row != 1 and p_col != 1) and board[0][2] == " ":  # Top Right
        weight = 0
        p = 3
    elif (p_row != 1 and p_col != 1) and board[1][0] == " ":  # Middle Left
        weight = 1
        p = 4
    elif (p_row != 1 and p_col != 1) and board[1][1] == " ":  # centre
        weight = 2
        p = 5
    elif (p_row != 1 and p_col != 1) and board[1][2] == " ":  # Middle Right
        weight = 1
        p = 6
    elif (p_row != 1 and p_col != 1) and board[2][0] == " ":  # Bottom Left
        weight = 0
        p = 7
    elif (p_row != 1 and p_col != 1) and board[2][1] == " ":  # Bottom Middle
        weight = 1
        p = 8
    elif (p_row != 1 and p_col != 1) and board[2][2] == " ":  # Bottom Right
        weight = 0
        p = 9

    if weight == 2:  # If centre is avalible chose it
        board[1][1] = "O"  # Place O
        crow = 300
        ccol = 300
        # all_moves(0, 0, False)

    elif weight == 1:  # If middle outside slots are avalible choose them
        if (p_row != 1 and p_col != 1) and board[0][1] == " ":  # If Top Middle is avalible choose it
            board[0][1] = "O"  # Place O
            crow = 300
            ccol = 0
            # all_moves(0, 0, False)
        elif (p_row != 1 and p_col != 1) and board[1][0] == " ":  # If Middle Left is avalible choose it
            board[1][0] = "O"  # Place O
            crow = 0
            ccol = 300
            # all_moves(0, 0, False)
        elif (p_row != 1 and p_col != 1) and board[1][2] == " ":  # If Middle Right is avalible choose it
            board[1][2] = "O"  # Place O
            crow = 600
            ccol = 300
            # all_moves(0, 0, False)
        elif (p_row != 1 and p_col != 1) and board[2][1] == " ":  # If Bottom Right is avalible choose it
            board[2][1] = "O"  # Place O
            crow = 300
            ccol = 600
            # all_moves(0, 0, False)

    elif weight == 0:
        if (p_row != 1 and p_col != 1) and board[0][0] == " ":  # If Top Left is avalible choose it
            board[0][0] = "O"  # Place O
            crow = 0
            ccol = 0
            # all_moves(0, 0, False)
        elif (p_row != 1 and p_col != 1) and board[0][2] == " ":  # If Top Right is avalible choose it
            board[0][2] = "O"  # Place O
            crow = 600
            ccol = 0
            # all_moves(0, 0, False)
        elif (p_row != 1 and p_col != 1) and board[2][0] == " ":  # If Bottom Left is avalible choose it
            board[2][0] = "O"  # Place O
            crow = 600
            ccol = 0
        #  all_moves(0, 0, False)
        elif (p_row != 1 and p_col != 1) and board[2][2] == " ":  # If Bottom Right is avalible choose it
            board[2][2] = "O"  # Place O
            crow = 600
            ccol = 600
            # all_moves(0, 0, False)


"""def all_moves(row, col, player_turn):
    global move_num
    if player_turn:  # If it is the players turn
        moves[row - 1][col - 1] = 1  # Add Move to all moves
    else:
        moves[row][col] = 0  # Add computers turn to all moves
    move_num += 1"""


def winning_moves():
    global move_num
    player_win = False
    comp_win = False

    # Player winning moves
    # Row wins
    if moves[0][0] == 1 and moves[0][1] == 1 and moves[0][2] == 1:
        player_win = True
    elif moves[1][0] == 1 and moves[1][1] == 1 and moves[1][2] == 1:
        player_win = True
    elif moves[2][0] == 1 and moves[2][1] == 1 and moves[2][2] == 1:
        player_win = True
    # Col wins
    if moves[0][0] == 1 and moves[1][0] == 1 and moves[2][0] == 1:
        player_win = True
    elif moves[0][1] == 1 and moves[1][1] == 1 and moves[2][1] == 1:
        player_win = True
    elif moves[0][2] == 1 and moves[1][2] == 1 and moves[2][2] == 1:
        player_win = True
    # Diagonal wins
    if moves[0][0] == 1 and moves[1][1] == 1 and moves[2][2] == 1:
        player_win = True
    elif moves[2][0] == 1 and moves[1][1] == 1 and moves[0][2] == 1:
        player_win = True

    # Computer winning moves
    # Row wins
    if moves[0][0] == 0 and moves[0][1] == 0 and moves[0][2] == 0:
        comp_win = True
    elif moves[1][0] == 0 and moves[1][1] == 0 and moves[1][2] == 0:
        comp_win = True
    elif moves[2][0] == 0 and moves[2][1] == 0 and moves[2][2] == 0:
        comp_win = True
    # Col wins
    if moves[0][0] == 0 and moves[1][0] == 0 and moves[2][0] == 0:
        comp_win = True
    elif moves[0][1] == 0 and moves[1][1] == 0 and moves[2][1] == 0:
        comp_win = True
    elif moves[0][2] == 0 and moves[1][2] == 0 and moves[2][2] == 0:
        comp_win = True
    # Diagonal wins
    if moves[0][0] == 0 and moves[1][1] == 0 and moves[2][2] == 0:
        comp_win = True
    elif moves[2][0] == 0 and moves[1][1] == 0 and moves[0][2] == 0:
        comp_win = True

    if player_win is True or comp_win is True:
        win(player_win, comp_win)


def win(pw, cw):
    global running
    if pw and cw:
        print("Tie")
    elif pw:
        print("player wins")
    elif cw:
        print("computer wins")
    else:
        print("No one wins")
    print(moves)
    running = False


XImg = pygame.image.load("X.png")
Xpos[i] = []

all_moves = [[0, 0], [300, 0], [600, 0],
             [0, 300], [300, 300], [600, 300],
             [0, 600], [300, 600], [600, 600]]

OposX = []
OposY = []


def drawX(x, y):
    Xpos[i].append(x)
    Xpos[i].append(y)


def addO(x, y):
    OposX.append(x)
    OposY.append(y)
    OImg = pygame.image.load("O.png")
    for i in range(len(OposX)):
        screen.blit(OImg, (OposX[i], OposY[i]))
    drawO()


def drawO():
    def pointer():  # The pointer
        global pointerX, pointerY
        if len(Xpos[i]) == 0:
            pointerImg = pygame.image.load("pointer.png")  # Load the image
            screen.blit(pointerImg, (pointerX, pointerY))
        else:
            for i in range(len(Xpos[i])):
                if pointerX == Xpos[i] and pointerY == Xpos[i][i]:
                    pointerImg = pygame.image.load("X overlap.png")  # load overlap image
                    screen.blit(pointerImg, (pointerX, pointerY))
                else:
                    pointerImg = pygame.image.load("pointer.png")  # Load normal image
                    screen.blit(pointerImg, (pointerX, pointerY))


def pointer():  # The pointer
    global pointerX, pointerY
    if len(Xpos[i]) == 0:
        pointerImg = pygame.image.load("pointer.png")  # Load the image
        screen.blit(pointerImg, (pointerX, pointerY))
    else:
        for i in range(len(Xpos[i])):
            if pointerX == Xpos[i][i] and pointerY == Xpos[i][i]:
                pointerImg = pygame.image.load("X overlap.png")  # load overlap image
                screen.blit(pointerImg, (pointerX, pointerY))
            else:
                pointerImg = pygame.image.load("pointer.png")  # Load normal image
                screen.blit(pointerImg, (pointerX, pointerY))


# Game loop
while running:
    winning_moves()

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
                #  if not (taken up by something):
                drawX(pointerX, pointerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                enemy_move(pointerX, pointerY)
    for i in range(len(Xpos[i])):
        screen.blit(XImg, (Xpos[i][i], Xpos[i][i]))  # Draw X
    pointer()
    addO(crow, ccol)
    pygame.display.update()
