import pygame
import random
import time

pygame.init()

SCREEN_SIZE = 400
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
FONT_COLOR = (119, 110, 101)
TIMER_FONT_COLOR = (255, 255, 255)
SCORE_FONT_COLOR = (255, 255, 255)


screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048")


font = pygame.font.Font(None, 55)
timer_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 36)


STATE_HOME = 0
STATE_GAME = 1
STATE_INSTRUCTIONS = 2
STATE_GAME_OVER = 3

def draw_board(board, score):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = board[i][j]
            tile_color = TILE_COLORS.get(tile_value, (60, 58, 50))
            pygame.draw.rect(screen, tile_color,
                             (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile_value != 0:
                text = font.render(str(tile_value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)
    score_text = score_font.render(f"Score: {score}", True, SCORE_FONT_COLOR)
    screen.blit(score_text, (SCREEN_SIZE - 150, 10))
    pygame.display.flip()

def initialize_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for _ in range(2):
        add_random_tile(board)
    return board

def add_random_tile(board):
    empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if not empty_tiles:
        return
    i, j = random.choice(empty_tiles)
    board[i][j] = random.choice([2, 4])

def slide_left(row):
    new_row = [0] * GRID_SIZE
    last = -1
    pos = 0
    score = 0
    for j in range(GRID_SIZE):
        if row[j] != 0:
            if last == row[j]:
                new_row[pos - 1] *= 2
                score += new_row[pos - 1]
                last = -1
            else:
                new_row[pos] = row[j]
                last = row[j]
                pos += 1
    return new_row, score

def move_left(board):
    new_board = []
    score = 0
    for row in board:
        new_row, row_score = slide_left(row)
        new_board.append(new_row)
        score += row_score
    if new_board != board:
        add_random_tile(new_board)
    return new_board, score

def reverse(board):
    new_board = [row[::-1] for row in board]
    return new_board

def transpose(board):
    new_board = [[board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    return new_board

def move_right(board):
    reversed_board = reverse(board)
    new_board, score = move_left(reversed_board)
    return reverse(new_board), score

def move_up(board):
    transposed_board = transpose(board)
    new_board, score = move_left(transposed_board)
    return transpose(new_board), score

def move_down(board):
    transposed_board = transpose(board)
    new_board, score = move_right(transposed_board)
    return transpose(new_board), score

def draw_home_page():
    screen.fill(BACKGROUND_COLOR)
    title_text = font.render("2048", True, FONT_COLOR)
    start_text = font.render("Press Enter to Start", True, FONT_COLOR)
    instructions_text = font.render("Press I for Instructions", True, FONT_COLOR)
    screen.blit(title_text, (SCREEN_SIZE // 2 - title_text.get_width() // 2, SCREEN_SIZE // 4))
    screen.blit(start_text, (SCREEN_SIZE // 2 - start_text.get_width() // 2, SCREEN_SIZE // 2))
    screen.blit(instructions_text, (SCREEN_SIZE // 2 - instructions_text.get_width() // 2, SCREEN_SIZE // 2 + 50))
    pygame.display.flip()

def draw_instructions_page():
    screen.fill(BACKGROUND_COLOR)
    instructions = [
        "2048 Game Instructions",
        "",
        "Use arrow keys to move tiles.",
        "Tiles with the same number merge",
        "into one when they touch.",
        "Add them up to reach 2048!"
    ]
    y = 50
    for line in instructions:
        text = font.render(line, True, FONT_COLOR)
        screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, y))
        y += 50
    back_text = font.render("Press Enter to go Back", True, FONT_COLOR)
    screen.blit(back_text, (SCREEN_SIZE // 2 - back_text.get_width() // 2, SCREEN_SIZE - 100))
    pygame.display.flip()

def draw_game_over_page(score):
    screen.fill(BACKGROUND_COLOR)
    game_over_text = font.render("Game Over", True, FONT_COLOR)
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    restart_text = font.render("Press Enter to Restart", True, FONT_COLOR)
    screen.blit(game_over_text, (SCREEN_SIZE // 2 - game_over_text.get_width() // 2, SCREEN_SIZE // 4))
    screen.blit(score_text, (SCREEN_SIZE // 2 - score_text.get_width() // 2, SCREEN_SIZE // 2))
    screen.blit(restart_text, (SCREEN_SIZE // 2 - restart_text.get_width() // 2, SCREEN_SIZE // 2 + 50))
    pygame.display.flip()

def main():
    state = STATE_HOME
    board = initialize_board()
    score = 0
    start_time = time.time()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == STATE_HOME:
                    if event.key == pygame.K_RETURN:
                        state = STATE_GAME
                        board = initialize_board()
                        score = 0
                        start_time = time.time()
                    elif event.key == pygame.K_i:
                        state = STATE_INSTRUCTIONS
                elif state == STATE_INSTRUCTIONS:
                    if event.key == pygame.K_RETURN:
                        state = STATE_HOME
                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        state = STATE_HOME
                elif state == STATE_GAME:
                    if event.key == pygame.K_LEFT:
                        board, move_score = move_left(board)
                        score += move_score
                    elif event.key == pygame.K_RIGHT:
                        board, move_score = move_right(board)
                        score += move_score
                    elif event.key == pygame.K_UP:
                        board, move_score = move_up(board)
                        score += move_score
                    elif event.key == pygame.K_DOWN:
                        board, move_score = move_down(board)
                        score += move_score

        if state == STATE_HOME:
            draw_home_page()
        elif state == STATE_INSTRUCTIONS:
            draw_instructions_page()
        elif state == STATE_GAME:
            draw_board(board, score)
            current_time = time.time()
            elapsed_time = current_time - start_time
            timer_text = timer_font.render(f"Time: {int(elapsed_time)}s", True, TIMER_FONT_COLOR)
            screen.blit(timer_text, (10, 10))
            pygame.display.flip()
            if all(tile != 0 for row in board for tile in row):
                state = STATE_GAME_OVER
        elif state == STATE_GAME_OVER:
            draw_game_over_page(score)

    pygame.quit()

if __name__ == "__main__":
    main()
