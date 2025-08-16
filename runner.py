import pygame
import sys
import math
from connect4 import (
    initial_state, current_player, actions, result,
    winner, terminal, minimax, RED, YELLOW, EMPTY, evaluate
)

# --- CONFIG ---
ROWS = 6
COLS = 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE  # top row for preview
FPS = 60

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 75)

# --- Drawing ---
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(
                screen, BLUE, (c*SQUARE_SIZE, (r+1)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            pygame.draw.circle(
                screen, BLACK,
                (c*SQUARE_SIZE + SQUARE_SIZE//2, (r+1)*SQUARE_SIZE + SQUARE_SIZE//2),
                RADIUS
            )

    for c in range(COLS):
        for r in range(ROWS):
            piece = board[r][c]
            if piece == RED:
                pygame.draw.circle(
                    screen, RED_COLOR,
                    (c*SQUARE_SIZE + SQUARE_SIZE//2, (r+1)*SQUARE_SIZE + SQUARE_SIZE//2),
                    RADIUS
                )
            elif piece == YELLOW:
                pygame.draw.circle(
                    screen, YELLOW_COLOR,
                    (c*SQUARE_SIZE + SQUARE_SIZE//2, (r+1)*SQUARE_SIZE + SQUARE_SIZE//2),
                    RADIUS
                )

    pygame.display.update()

# --- Helpers ---
def get_col_from_mouse(x):
    return x // SQUARE_SIZE

# --- Game State ---
board = initial_state()
human_player = RED   # Human is red, AI is yellow
game_over = False

draw_board(board)

# --- Game Loop ---
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over:
            continue

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            posx = event.pos[0]
            color = RED_COLOR if current_player(board) == RED else YELLOW_COLOR
            pygame.draw.circle(screen, color, (posx, SQUARE_SIZE//2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_player(board) == human_player:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                col = get_col_from_mouse(event.pos[0])

                # Find the valid action in this column
                for action in actions(board):
                    if action[1] == col:  # action is (row, col)
                        board = result(board, action)
                        break

                draw_board(board)

                if winner(board):
                    label = font.render("You win!", True, RED_COLOR)
                    screen.blit(label, (40, 10))
                    game_over = True
                elif terminal(board):
                    label = font.render("Draw!", True, (255, 255, 255))
                    screen.blit(label, (40, 10))
                    game_over = True

    # AI Turn
    if not game_over and current_player(board) != human_player:
        pygame.time.wait(500)
        ai_action = minimax(board)
        if ai_action:
            board = result(board, ai_action)

        draw_board(board)

        if winner(board):
            label = font.render("AI wins!", True, YELLOW_COLOR)
            screen.blit(label, (40, 10))
            game_over = True
        elif terminal(board):
            label = font.render("Draw!", True, (255, 255, 255))
            screen.blit(label, (40, 10))
            game_over = True

    if game_over:
        pygame.display.update()
        pygame.time.wait(3000)
