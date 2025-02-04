import pygame
import sys

WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
CELL_SIZE = WIDTH // BOARD_COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

PLAYER = "X"
AI = "O"

# Create a board
board = [["" for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Draw the grid
def draw_grid():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_marks():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == PLAYER:
                pygame.draw.line(screen, BLUE, (col * CELL_SIZE + 20, row * CELL_SIZE + 20), 
                                 ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
                pygame.draw.line(screen, BLUE, ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20), 
                                 (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), LINE_WIDTH)
            elif board[row][col] == AI:
                pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 
                                   CELL_SIZE // 3, LINE_WIDTH)

# Check if there is a winner
def check_winner():
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != "":
            return board[row][0]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    return None

# Check if the board is full
def is_full():
    for row in board:
        if "" in row:
            return False
    return True

# Algorithm for AI
def minimax(is_maximizing):
    winner = check_winner()
    if winner == PLAYER:
        return -1
    if winner == AI:
        return 1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == "":
                    board[row][col] = AI
                    score = minimax(False)
                    board[row][col] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == "":
                    board[row][col] = PLAYER
                    score = minimax(True)
                    board[row][col] = ""
                    best_score = min(score, best_score)
        return best_score

# AI turn
def ai_move():
    best_score = -float("inf")
    best_move = None

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "":
                board[row][col] = AI
                score = minimax(False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        board[best_move[0]][best_move[1]] = AI

# Loop of the game
running = True
game_over = False

draw_grid()
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE

            if board[row][col] == "":
                board[row][col] = PLAYER
                winner = check_winner()
                if winner or is_full():
                    game_over = True
                else:
                    ai_move()
                    winner = check_winner()
                    if winner or is_full():
                        game_over = True

    screen.fill(WHITE)
    draw_grid()
    draw_marks()
    pygame.display.flip()

    if game_over:
        print(f"Winner: {winner if winner else ' Tie'}")
        pygame.time.delay(2000)  
        running = False

pygame.quit()
sys.exit()
