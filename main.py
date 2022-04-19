import pygame
from dataclasses import dataclass
import random

pygame.init()

ROWS = 20
COLS = 10
OFFSET_X = 35
OFFSET_Y = 35
WIDTH = 400
SPACE = WIDTH // COLS
HEIGHT = (SPACE * ROWS)
BG_COLOR = "black"
FPS = 30
SPEED = 600

win = pygame.display.set_mode((WIDTH + (2 * OFFSET_X), HEIGHT + (2 * OFFSET_Y)))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
pygame.key.set_repeat(100)


pieces = [pygame.transform.scale(pygame.image.load(
    f"./assets/piece_{i}.png"), (SPACE, SPACE)) for i in range(1, 10)]
background = pygame.transform.scale(pygame.image.load("./assets/background.png"), (WIDTH + (2 * OFFSET_X), HEIGHT + (2 * OFFSET_Y)))

TETROMINOES = [
    [0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

grid = [0] * WIDTH * HEIGHT


# User events
SHAPE_DOWN = pygame.USEREVENT+1
pygame.time.set_timer(SHAPE_DOWN, SPEED)


@dataclass
class Tetrominoe():
    shape: list
    row: int = 0
    col: int = 4

    def show(self):
        x = self.col * SPACE
        y = self.row * SPACE
        for i, color in enumerate(self.shape):
            if color > 0:
                x = OFFSET_X + ((i % 4 + self.col) * SPACE)
                y = OFFSET_Y + ((i // 4 + self.row) * SPACE)
                win.blit(pieces[color], (x, y))

    def __is_valid_move(self, row, col):
        for i, color in enumerate(self.shape):
            if color > 0:
                r = row + i // 4
                c = col + i % 4
                if c < 0 or c >= COLS or r >= ROWS or grid[r * COLS + c] > 0:
                    return False
        return True

    def move(self, delta_row, delta_col):
        if self.__is_valid_move(self.row + delta_row, self.col + delta_col):
            self.row += delta_row
            self.col += delta_col
            return True

    def rotate(self):
        shape_copy = self.shape.copy()
        for n, color in enumerate(shape_copy):
            r = n // 4
            c = n % 4
            self.shape[(2-c)*4+r] = color
        if not self.__is_valid_move(self.row, self.col):
            self.shape = shape_copy


def shape_to_grid(shape):
    for i, color in enumerate(shape.shape):
        if color > 0:
            r, c = shape.row + i // 4, shape.col + i % 4
            grid[r * COLS + c] = color


def delete_lines():
    global grid
    new_grid = grid.copy()
    for row in range(ROWS)[::-1]:
        while grid[row * COLS: (row + 1) * COLS].count(0) == 0:
            print(row)
            grid[0: (row+1) * COLS] = [0] * COLS + grid[0:row * COLS]


def draw(shape):
    clock.tick(FPS)

    # draw background
    win.blit(background, (0, 0))

    # draw main shape that is falling
    shape.show()

    # draw grid
    for i, color in enumerate(grid):
        if color > 0:
            x = (i % COLS) * SPACE + OFFSET_X
            y = (i // COLS) * SPACE + OFFSET_Y
            win.blit(pieces[color], (x, y))

    pygame.display.update()


def run():
    running = True

    shape = Tetrominoe(random.choice(TETROMINOES))

    while running:
        # Game Logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SHAPE_DOWN:
                if not shape.move(1, 0):
                    shape_to_grid(shape)
                    delete_lines()
                    del shape
                    shape = Tetrominoe(random.choice(TETROMINOES))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    shape.move(0, 1)
                if event.key == pygame.K_DOWN:
                    shape.move(1, 0)
                if event.key == pygame.K_LCTRL:
                    shape.rotate()

        draw(shape)

    pygame.quit()


run()
