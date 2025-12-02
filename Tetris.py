# ...existing code...
"""
간단한 Tetris (Pygame)
실행: python c:\work\Tetris.py
필요: pip install pygame
"""
import pygame
import random
import sys

pygame.init()
# 화면 설정
BLOCK_SIZE = 30
COLS, ROWS = 10, 20
SIDE_WIDTH = 6 * BLOCK_SIZE
WIDTH = COLS * BLOCK_SIZE + SIDE_WIDTH
HEIGHT = ROWS * BLOCK_SIZE
FPS = 60

# 색상
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [
    (0, 240, 240),  # I
    (0, 0, 240),    # J
    (240, 160, 0),  # L
    (240, 240, 0),  # O
    (0, 240, 0),    # S
    (160, 0, 240),  # T
    (240, 0, 0),    # Z
]

# 블록 모양 (회전 상태 목록)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for (col, row), color in locked_positions.items():
        if 0 <= row < ROWS and 0 <= col < COLS:
            grid[row][col] = color
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted = [(c, r) for r in range(ROWS) for c in range(COLS) if grid[r][c] == BLACK]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted:
            if pos[1] >= 0:
                return False
    return True

def check_lost(positions):
    for (col, row) in positions:
        if row < 1:
            return True
    return False

def get_shape():
    return Piece(COLS // 2, 0, random.choice(SHAPES))

def clear_rows(grid, locked):
    inc = 0
    for i in range(ROWS - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            # 지운 줄의 블록들을 locked에서 제거
            for j in range(COLS):
                try:
                    del locked[(j, i)]
                except:
                    pass
    if inc > 0:
        # 위의 블록들을 아래로 이동
        new_locked = {}
        for (x, y), col in sorted(locked.items(), key=lambda x: x[0][1], reverse=True):
            shift = 0
            for i in range(ROWS - 1, -1, -1):
                if i < y and all((j, i) not in locked for j in range(COLS)):
                    pass
            new_locked[(x, y + inc)] = col
        locked.clear()
        locked.update(new_locked)
    return inc

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))

def draw_grid(surface, grid):
    for i in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, i * BLOCK_SIZE), (COLS * BLOCK_SIZE, i * BLOCK_SIZE))
        for j in range(COLS):
            pygame.draw.line(surface, GRAY, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, ROWS * BLOCK_SIZE))

def draw_window(surface, grid, score=0, level=1):
    surface.fill(BLACK)
    # 플레이 영역 블록 그리기
    for i in range(ROWS):
        for j in range(COLS):
            pygame.draw.rect(surface, grid[i][j],
                             (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    # 그리드 선
    draw_grid(surface, grid)
    # 사이드 패널 (점수, 다음 블록)
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', True, WHITE)
    surface.blit(label, (COLS * BLOCK_SIZE + 20, 20))
    label2 = font.render(f'Level: {level}', True, WHITE)
    surface.blit(label2, (COLS * BLOCK_SIZE + 20, 60))

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 25)
    label = font.render('Next:', True, WHITE)
    sx = COLS * BLOCK_SIZE + 20
    sy = 120
    surface.blit(label, (sx, sy))
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == '0':
                pygame.draw.rect(surface, piece.color,
                                 (sx + j * BLOCK_SIZE, sy + 30 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # 초마다 한 칸
    level = 1
    score = 0

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    pygame.time.set_timer(pygame.USEREVENT + 1, int(fall_speed * 1000))

    while run:
        grid = create_grid(locked_positions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    # Hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
                elif event.key == pygame.K_p:
                    # Pause
                    paused = True
                    draw_text_middle(screen, "Paused - Press P", 40, WHITE)
                    pygame.display.update()
                    while paused:
                        for e in pygame.event.get():
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                                paused = False
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
            if event.type == pygame.USEREVENT + 1:
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)
        for (x, y) in shape_pos:
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # 줄 삭제 & 점수
            cleared = clear_rows(grid, locked_positions)
            if cleared > 0:
                score += (cleared ** 2) * 100
                level = score // 1000 + 1
                # 속도 증가
                fall_speed = max(0.1, 0.5 - (level - 1) * 0.02)
                pygame.time.set_timer(pygame.USEREVENT + 1, int(fall_speed * 1000))

        draw_window(screen, grid, score, level)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(screen, "GAME OVER", 60, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

        clock.tick(FPS)

def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris - Press Any Key to Start')
    run = True
    while run:
        screen.fill(BLACK)
        draw_text_middle(screen, "Press Any Key to Play", 40, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

if __name__ == '__main__':
    main_menu()
# ...existing code...