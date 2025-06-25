import pygame
import random
import os
import tkinter as tk

pygame.font.init()

s_width = 600
s_height = 800
col = 10
row = 20

block_size = 25

play_width = col * block_size
play_height = row * block_size

top_left_x = 270
top_left_y = 90

filepath = 'media/tetris/highscore.txt'
fontpath = 'media/tetris/arcade.ttf'
fontpath_mario = 'media/tetris/mario.ttf'

S = [['.....','.....','..00.','.00..','.....'], ['.....','..0..','..00.','...0.','.....']]
Z = [['.....','.....','.00..','..00.','.....'], ['.....','..0..','.00..','.0...','.....']]
I = [['.....','..0..','..0..','..0..','..0..'], ['.....','0000.','.....','.....','.....']]
O = [['.....','.....','.00..','.00..','.....']]
J = [['.....','.0...','.000.','.....','.....'], ['.....','..00.','..0..','..0..','.....'],
     ['.....','.....','.000.','...0.','.....'], ['.....','..0..','..0..','.00..','.....']]
L = [['.....','...0.','.000.','.....','.....'], ['.....','..0..','..0..','..00.','.....'],
     ['.....','.....','.000.','.0...','.....'], ['.....','.00..','..0..','..0..','.....']]
T = [['.....','..0..','.000.','.....','.....'], ['.....','..0..','..00.','..0..','.....'],
     ['.....','.....','.000.','..0..','.....'], ['.....','..0..','.00..','..0..','.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,165,0),(0,0,255),(128,0,128)]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked={}):
    grid = [[(0,0,0) for _ in range(col)] for _ in range(row)]

    for y in range(row):
        for x in range(col):
            if (x, y) in locked:
                grid[y][x] = locked[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    shape = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape):
        for j, char in enumerate(list(line)):
            if char == '0':
                positions.append((piece.x + j, piece.y + i))
    return [(x - 2, y - 4) for x, y in positions]

def valid_space(piece, grid):
    accepted = [(x, y) for y in range(row) for x in range(col) if grid[y][x] == (0,0,0)]

    for pos in convert_shape_format(piece):
        if pos not in accepted and pos[1] >= 0:
            return False
    return True

def check_lost(positions):
    return any(y < 1 for _, y in positions)

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, True, color)
    surface.blit(label, (top_left_x + play_width//2 - label.get_width()//2, top_left_y + play_height//2 - label.get_height()//2))

def draw_text_centered(surface, text, size, color, x, y):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, True, color)
    surface.blit(label, (x - label.get_width() // 2, y - label.get_height() // 2))

def draw_grid(surface):
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))

    for j in range(col):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * block_size, top_left_y),
                         (top_left_x + j * block_size, top_left_y + play_height))

def clear_rows(grid, locked):
    inc = 0
    full_rows_indices = []

    for i in range(row - 1, -1, -1):
        if (0, 0, 0) not in grid[i]:
            full_rows_indices.append(i)
            inc += 1

    if inc == 0:
        return 0
    new_locked = {}

    for (x, y), color in locked.items():
        shift_amount = 0

        for full_row_idx in full_rows_indices:
            if y < full_row_idx:
                shift_amount += 1

        if y not in full_rows_indices:
            new_locked[(x, y + shift_amount)] = color

    locked.clear()
    locked.update(new_locked)

    return inc

def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', True, (255,255,255))
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height//2 - 100

    for i, line in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
        for j, char in enumerate(list(line)):
            if char == '0':
                pygame.draw.rect(surface, piece.color,
                                 (start_x + j * block_size, start_y + i * block_size,
                                  block_size, block_size), 0, 5)
    surface.blit(label, (start_x, start_y - 30))

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0,0,0))

    font = pygame.font.Font(fontpath_mario, 65)
    label = font.render('TETRIS', True, (255,255,255))

    surface.blit(label, (top_left_x + play_width//2 - label.get_width()//2, 30))

    font = pygame.font.Font(fontpath, 30)

    surface.blit(font.render('SCORE   ' + str(score), True, (255,255,255)), (top_left_x + play_width + 50, top_left_y + play_height//2 + 100))
    surface.blit(font.render('HIGHSCORE   ' + str(last_score), True, (255,255,255)), (top_left_x - 200, top_left_y + play_height//2 + 100))

    for i in range(row):
        for j in range(col):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size,
                              block_size, block_size), 0, 3)

    draw_grid(surface)
    pygame.draw.rect(surface, (255,255,255), (top_left_x, top_left_y, play_width, play_height), 4, 10)

def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        file.write(str(max(new_score, score)))

def get_max_score():
    try:
        with open(filepath, 'r') as file:
            return int(file.readline())
    except:
        return 0

def main(root):
    pygame.init()
    os.environ['SDL_WINDOWID'] = str(root.winfo_id())
    pygame.display.init()
    screen = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Tetris")

    locked = {}
    change = False
    run = True
    game_over = False
    current = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    screen.fill((0, 0, 0))
    draw_text_middle("Press any key to start", 40, (255, 255, 255), screen)
    pygame.display.update()

    waiting_for_start = True

    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_start = False
            elif event.type == pygame.QUIT:
                pygame.quit()

                return

    while run:
        grid = create_grid(locked)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if not game_over:
            if level_time / 1000 > 5:
                level_time = 0

                if fall_speed > 0.15:
                    fall_speed -= 0.005

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                current.y += 1

                if not valid_space(current, grid):
                    current.y -= 1
                    change = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current.x -= 1

                        if not valid_space(current, grid):
                            current.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current.x += 1

                        if not valid_space(current, grid):
                            current.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current.y += 1

                        if not valid_space(current, grid):
                            current.y -= 1
                    elif event.key == pygame.K_UP:
                        current.rotation = (current.rotation + 1) % len(current.shape)

                        if not valid_space(current, grid):
                            current.rotation = (current.rotation - 1) % len(current.shape)

            for x, y in convert_shape_format(current):
                if y >= 0:
                    grid[y][x] = current.color

            if change:
                for pos in convert_shape_format(current):
                    locked[pos] = current.color
                current = next_piece
                next_piece = get_shape()
                change = False
                score += clear_rows(grid, locked) * 10
                update_score(score)

                if last_score < score:
                    last_score = score

            draw_window(screen, grid, score, last_score)
            draw_next_shape(next_piece, screen)
            pygame.display.update()

            if check_lost(locked):
                game_over = True

        else:
            screen.fill((0, 0, 0))
            draw_text_centered(screen, "You Lost", 50, (255, 0, 0), s_width // 2 + 100, s_height // 2 - 110)
            draw_text_centered(screen, "Press R to Restart or ESC to Quit", 30, (255, 255, 255), s_width // 2 + 100,
                               s_height // 2 - 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        locked = {}
                        change = False
                        game_over = False
                        current = get_shape()
                        next_piece = get_shape()
                        fall_time = 0
                        fall_speed = 0.35
                        level_time = 0
                        score = 0
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                elif event.type == pygame.QUIT:
                    run = False

    pygame.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tetris")
    root.geometry(f"{s_width}x{s_height}")

    embed = tk.Frame(root, width=s_width, height=s_height)
    embed.pack()

    root.update()

    main(embed)

    root.mainloop()
