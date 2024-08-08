import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Constants
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
ANIMATION_TIME = 200

# Initialize screen and fonts
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 55)
timer_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 36)

# Game states
STATE_HOME = 0
STATE_GAME = 1
STATE_INSTRUCTIONS = 2
STATE_GAME_OVER = 3

# Load sounds
def load_sounds():
    sounds = {
        'game_start': pygame.mixer.Sound('audio/game_start.mp3'),
        'move': pygame.mixer.Sound('audio/move.mp3'),
        'game_over': pygame.mixer.Sound('audio/game_over.mp3'),
        'bg_music': 'audio/bg_music.mp3'
    }
    pygame.mixer.music.load(sounds['bg_music'])
    pygame.mixer.music.play(-1)
    return sounds

# Draw functions
def draw_text(text, size, color, position, center=True):
    font_obj = pygame.font.Font(None, size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = position
    else:
        text_rect.topleft = position
    screen.blit(text_surface, text_rect)

def draw_board(board, score, moving_tiles, elapsed_time, animations_enabled):
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = board[i][j]
            tile_color = TILE_COLORS.get(tile_value, (60, 58, 50))
            pygame.draw.rect(screen, tile_color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile_value != 0:
                draw_text(str(tile_value), 55, FONT_COLOR, (j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))

    if animations_enabled:
        for tile in moving_tiles:
            if len(tile) == 3:
                start_pos, end_pos, value = tile
                start_x, start_y = start_pos
                end_x, end_y = end_pos
                progress = min(elapsed_time / ANIMATION_TIME, 1)
                current_x = start_x + (end_x - start_x) * progress
                current_y = start_y + (end_y - start_y) * progress
                tile_color = TILE_COLORS.get(value, (60, 58, 50))
                pygame.draw.rect(screen, tile_color, (current_x * TILE_SIZE, current_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                draw_text(str(value), 55, FONT_COLOR, (current_x * TILE_SIZE + TILE_SIZE // 2, current_y * TILE_SIZE + TILE_SIZE // 2))

    draw_text(f"Score: {score}", 36, SCORE_FONT_COLOR, (SCREEN_SIZE - 150, 10), center=False)
    pygame.display.flip()

def draw_home_page():
    screen.fill(BACKGROUND_COLOR)
    draw_text("2048", 55, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE // 4))
    draw_text("Press Enter to Start", 36, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    draw_text("Press I for Instructions", 36, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 50))
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
        draw_text(line, 36, FONT_COLOR, (SCREEN_SIZE // 2, y))
        y += 50
    draw_text("Press Enter to go Back", 36, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE - 100))
    pygame.display.flip()

def draw_game_over_page(score):
    screen.fill(BACKGROUND_COLOR)
    draw_text("Game Over", 55, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE // 4))
    draw_text(f"Score: {score}", 36, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    draw_text("Press Enter to Restart", 36, FONT_COLOR, (SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 50))
    pygame.display.flip()

# Game logic functions
def initialize_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for _ in range(2):
        add_random_tile(board)
    return board

def add_random_tile(board):
    empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = random.choice([2, 4])

def slide_and_combine(row):
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

def move(board, direction):
    def reverse(board):
        return [row[::-1] for row in board]

    def transpose(board):
        return [[board[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

    move_operations = {
        'left': lambda b: b,
        'right': reverse,
        'up': lambda b: transpose(b),
        'down': lambda b: reverse(transpose(b))
    }

    inverse_operations = {
        'left': lambda b: b,
        'right': reverse,
        'up': lambda b: transpose(b),
        'down': lambda b: transpose(reverse(b))
    }

    transformed_board = move_operations[direction](board)
    new_board = []
    score = 0
    moves = []
    for row in transformed_board:
        new_row, row_score, row_moves = slide_and_combine(row)
        new_board.append(new_row)
        score += row_score
        moves.extend(row_moves)
    new_board = inverse_operations[direction](new_board)
    if new_board != board:
        add_random_tile(new_board)
    return new_board, score, moves

def main():
    state = STATE_HOME
    board = initialize_board()
    score = 0
    start_time = time.time()
    moving_tiles = []
    animation_start_time = None
    animations_enabled = True
    sounds = load_sounds()
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
                elif state == STATE_GAME:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        direction_map = {
                            pygame.K_LEFT: 'left',
                            pygame.K_RIGHT: 'right',
                            pygame.K_UP: 'up',
                            pygame.K_DOWN: 'down'
                        }
                        direction = direction_map[event.key]
                        board, move_score, move_tiles = move(board, direction)
                        score += move_score
                        if animations_enabled:
                            moving_tiles = [((j, i), (move_tiles[j], i), board[i][move_tiles[j]]) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][move_tiles[j]] != 0]
                            animation_start_time = time.time()
                        else:
                            moving_tiles = []
                        sounds['move'].play()
                        if any(2048 in row for row in board):
                            state = STATE_GAME_OVER
                            sounds['game_over'].play()
                    elif event.key == pygame.K_r:
                        state = STATE_HOME
                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        state = STATE_HOME

        if state == STATE_GAME and animations_enabled and moving_tiles:
            elapsed_time = time.time() - animation_start_time
        else:
            elapsed_time = 0

        if state == STATE_HOME:
            draw_home_page()
        elif state == STATE_INSTRUCTIONS:
            draw_instructions_page()
        elif state == STATE_GAME:
            draw_board(board, score, moving_tiles, elapsed_time, animations_enabled)
        elif state == STATE_GAME_OVER:
            draw_game_over_page(score)

if __name__ == "__main__":
    main()
