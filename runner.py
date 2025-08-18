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
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 50)
small_font = pygame.font.SysFont("monospace", 25)
tiny_font = pygame.font.SysFont("monospace", 20)

# --- Game States ---
MENU = 0
PLAYING = 1
GAME_OVER = 2

game_state = MENU
board = None
human_player = None
game_over = False


def draw_menu():
    """Draw the color selection menu"""
    screen.fill(BLACK)

    # Title
    title = font.render("Connect 4", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    screen.blit(title, title_rect)

    # Instructions
    instruction = small_font.render("Choose your color:", True, WHITE)
    instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(instruction, instruction_rect)

    # Red button
    red_button = pygame.Rect(WIDTH // 4 - 60, HEIGHT // 2 - 30, 120, 60)
    pygame.draw.rect(screen, RED_COLOR, red_button)
    pygame.draw.rect(screen, WHITE, red_button, 2)
    red_text = small_font.render("RED", True, WHITE)
    red_text_rect = red_text.get_rect(center=red_button.center)
    screen.blit(red_text, red_text_rect)

    # Yellow button
    yellow_button = pygame.Rect(3 * WIDTH // 4 - 60, HEIGHT // 2 - 30, 120, 60)
    pygame.draw.rect(screen, YELLOW_COLOR, yellow_button)
    pygame.draw.rect(screen, BLACK, yellow_button, 2)
    yellow_text = small_font.render("YELLOW", True, BLACK)
    yellow_text_rect = yellow_text.get_rect(center=yellow_button.center)
    screen.blit(yellow_text, yellow_text_rect)

    # Additional info
    info = tiny_font.render("RED plays first", True, GRAY)
    info_rect = info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(info, info_rect)

    pygame.display.update()

    return red_button, yellow_button


def handle_menu_click(pos, red_button, yellow_button):
    """Handle clicks on the menu buttons"""
    global game_state, board, human_player

    if red_button.collidepoint(pos):
        human_player = RED
        game_state = PLAYING
        board = initial_state()
        return True
    elif yellow_button.collidepoint(pos):
        human_player = YELLOW
        game_state = PLAYING
        board = initial_state()
        return True
    return False


def draw_board(board):
    """Draw the game board"""
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(
                screen, BLUE, (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            )
            pygame.draw.circle(
                screen, BLACK,
                (c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                RADIUS
            )

    for c in range(COLS):
        for r in range(ROWS):
            piece = board[r][c]
            if piece == RED:
                pygame.draw.circle(
                    screen, RED_COLOR,
                    (c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                    RADIUS
                )
            elif piece == YELLOW:
                pygame.draw.circle(
                    screen, YELLOW_COLOR,
                    (c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                    RADIUS
                )

    pygame.display.update()


def get_col_from_mouse(x):
    """Convert mouse x coordinate to column"""
    return x // SQUARE_SIZE


def reset_game():
    """Reset the game to menu state"""
    global game_state, board, human_player, game_over
    game_state = MENU
    board = None
    human_player = None
    game_over = False


# --- Main Game Loop ---
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state == GAME_OVER:
                reset_game()
                continue

        if game_state == MENU:
            red_button, yellow_button = draw_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_menu_click(event.pos, red_button, yellow_button):
                    draw_board(board)

        elif game_state == PLAYING:
            if event.type == pygame.MOUSEMOTION and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                color = RED_COLOR if current_player(board) == RED else YELLOW_COLOR
                pygame.draw.circle(screen, color, (posx, SQUARE_SIZE // 2), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
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
                        win_color = RED_COLOR if human_player == RED else YELLOW_COLOR
                        label = font.render("You win!", True, win_color)
                        screen.blit(label, (20, 10))

                        # Show restart instruction
                        restart_label = tiny_font.render("Press R to restart", True, WHITE)
                        screen.blit(restart_label, (20, 70))
                        pygame.display.update()

                        game_over = True
                        game_state = GAME_OVER
                    elif terminal(board):
                        label = font.render("Draw!", True, WHITE)
                        screen.blit(label, (20, 10))

                        # Show restart instruction
                        restart_label = tiny_font.render("Press R to restart", True, WHITE)
                        screen.blit(restart_label, (20, 70))
                        pygame.display.update()

                        game_over = True
                        game_state = GAME_OVER

    # AI Turn
    if game_state == PLAYING and not game_over and current_player(board) != human_player:
        pygame.time.wait(500)
        ai_action = minimax(board)
        if ai_action:
            board = result(board, ai_action)

        draw_board(board)

        if winner(board):
            ai_color = YELLOW_COLOR if human_player == RED else RED_COLOR
            label = font.render("AI wins!", True, ai_color)
            screen.blit(label, (20, 10))

            # Show restart instruction
            restart_label = tiny_font.render("Press R to restart", True, WHITE)
            screen.blit(restart_label, (20, 70))
            pygame.display.update()

            game_over = True
            game_state = GAME_OVER
        elif terminal(board):
            label = font.render("Draw!", True, WHITE)
            screen.blit(label, (20, 10))

            # Show restart instruction
            restart_label = tiny_font.render("Press R to restart", True, WHITE)
            screen.blit(restart_label, (20, 70))
            pygame.display.update()

            game_over = True
            game_state = GAME_OVER

    # Keep menu displayed when in menu state
    if game_state == MENU:
        draw_menu()