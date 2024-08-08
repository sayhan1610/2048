import pygame
import random
import time

pygame.init()
pygame.mixer.init()

SCREEN_SIZE = 600
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE
BACKGROUND_COLOR = (30, 30, 30)
TILE_COLORS = {
    0: (50, 50, 50),
    2: (255, 87, 34),
    4: (255, 195, 0),
    8: (244, 67, 54),
    16: (76, 175, 80),
    32: (33, 150, 243),
    64: (156, 39, 176),
    128: (63, 81, 181),
    256: (0, 188, 212),
    512: (3, 169, 244),
    1024: (0, 150, 136),
    2048: (255, 235, 59)
}
FONT_COLOR = (255, 255, 255)
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

ANIMATION_TIME = 200

# Load sounds
sounds = {
    'game_start': pygame.mixer.Sound('audio/game_start.mp3'),
    'bg_music': 'audio/bg_music.mp3',
    'move': pygame.mixer.Sound('audio/move.mp3'),
    'game_over': pygame.mixer.Sound('audio/game_over.mp3')
}

# Play background music
pygame.mixer.music.load(sounds['bg_music'])
pygame.mixer.music.play(-1)

def draw_board(board, score, moving_tiles, elapsed_time, animations_enabled):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = board[i][j]
            tile_color = TILE_COLORS.get(tile_value, (60, 58, 50))
            pygame.draw.rect(screen, tile_color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile_value != 0:
                text = font.render(str(tile_value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

    if animations_enabled:
        for (start_pos, end_pos, value) in moving_tiles:
            if len(start_pos) == 2 and len(end_pos) == 2:
                start_x, start_y = start_pos
                end_x, end_y = end_pos
                progress = min(elapsed_time / ANIMATION_TIME, 1)
                current_x = start_x + (end_x - start_x) * progress
                current_y = start_y + (end_y - start_y) * progress
                tile_color = TILE_COLORS.get(value, (60, 58, 50))
                pygame.draw.rect(screen, tile_color, (current_x * TILE_SIZE, current_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(current_x * TILE_SIZE + TILE_SIZE // 2, current_y * TILE_SIZE + TILE_SIZE // 2))
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
    moves = []
    for j in range(GRID_SIZE):
        if row[j] != 0:
            if last == row[j]:
                new_row[pos - 1] *= 2
                score += new_row[pos - 1]
                last = -1
            else:
                new_row[pos] = row[j]
                if pos != j:
                    moves.append((j, pos))
                last = row[j]
                pos += 1
    return new_row, score, moves

def move_left(board):
    new_board = []
    score = 0
    moves = []
    for i, row in enumerate(board):
        new_row, row_score, row_moves = slide_left(row)
        new_board.append(new_row)
        score += row_score
        for j, k in row_moves:
            moves.append(((i, j), (i, k), row[j]))
    if new_board != board:
        add_random_tile(new_board)
    return new_board, score, moves

def reverse(board):
    return [row[::-1] for row in board]

def transpose(board):
    return [[board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

def move_right(board):
    reversed_board = reverse(board)
    new_board, score, moves = move_left(reversed_board)
    new_board = reverse(new_board)
    moves = [((x, GRID_SIZE - 1 - y1), (x, GRID_SIZE - 1 - y2), value) for ((x, y1), (x, y2), value) in moves]
    return new_board, score, moves

def move_up(board):
    transposed_board = transpose(board)
    new_board, score, moves = move_left(transposed_board)
    new_board = transpose(new_board)
    moves = [((y, x1), (y, x2), value) for ((x1, y), (x2, y), value) in moves]
    return new_board, score, moves

def move_down(board):
    transposed_board = transpose(board)
    new_board, score, moves = move_right(transposed_board)
    new_board = transpose(new_board)
    moves = [((y, x1), (y, x2), value) for ((x1, y), (x2, y), value) in moves]
    return new_board, score, moves

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
        "Add them up to reach 2048!",
        "",
        "Press D to toggle animations."
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
    moving_tiles = []
    animation_start_time = None
    animations_enabled = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    animations_enabled = not animations_enabled
                    moving_tiles = []
                elif state == STATE_HOME:
                    if event.key == pygame.K_RETURN:
                        state = STATE_GAME
                        board = initialize_board()
                        score = 0
                        start_time = time.time()
                        sounds['game_start'].play()
                    elif event.key == pygame.K_i:
                        state = STATE_INSTRUCTIONS
                elif state == STATE_INSTRUCTIONS:
                    if event.key == pygame.K_RETURN:
                        state = STATE_HOME
                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        state = STATE_HOME
                        sounds['game_start'].play()
                elif state == STATE_GAME:
                    if not moving_tiles:
                        if event.key == pygame.K_LEFT:
                            board, move_score, moves = move_left(board)
                        elif event.key == pygame.K_RIGHT:
                            board, move_score, moves = move_right(board)
                        elif event.key == pygame.K_UP:
                            board, move_score, moves = move_up(board)
                        elif event.key == pygame.K_DOWN:
                            board, move_score, moves = move_down(board)
                        if moves:
                            score += move_score
                            moving_tiles = moves
                            sounds['move'].play()
                            if animations_enabled:
                                animation_start_time = pygame.time.get_ticks()
                            else:
                                moving_tiles = [] 

        if state == STATE_HOME:
            draw_home_page()
        elif state == STATE_INSTRUCTIONS:
            draw_instructions_page()
        elif state == STATE_GAME:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if animations_enabled and moving_tiles:
                animation_elapsed_time = pygame.time.get_ticks() - animation_start_time
                if animation_elapsed_time >= ANIMATION_TIME:
                    moving_tiles = []
                draw_board(board, score, moving_tiles, animation_elapsed_time, animations_enabled)
            else:
                draw_board(board, score, [], 0, animations_enabled)
            timer_text = timer_font.render(f"Time: {int(elapsed_time)}s", True, TIMER_FONT_COLOR)
            screen.blit(timer_text, (10, 10))
            pygame.display.flip()
            if all(tile != 0 for row in board for tile in row):
                state = STATE_GAME_OVER
                sounds['game_over'].play()
        elif state == STATE_GAME_OVER:
            draw_game_over_page(score)

    pygame.quit()

if __name__ == "__main__":
    main()
