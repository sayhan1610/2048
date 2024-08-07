import pygame
import random


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

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("2048")


font = pygame.font.Font(None, 55)

def draw_board(board):
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

def slide_left(board):
    def merge(row):
        new_row = [0] * GRID_SIZE
        last = -1
        pos = 0
        for j in range(GRID_SIZE):
            if row[j] != 0:
                if last == row[j]:
                    new_row[pos - 1] *= 2
                    last = -1
                else:
                    new_row[pos] = row[j]
                    last = row[j]
                    pos += 1
        return new_row

    new_board = [merge(row) for row in board]
    return new_board

def move_left(board):
    new_board = slide_left(board)
    if new_board != board:
        add_random_tile(new_board)
    return new_board

def main():
    board = initialize_board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board = move_left(board)
        draw_board(board)

    pygame.quit()

if __name__ == "__main__":
    main()
