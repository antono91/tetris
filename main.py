import pygame
from dataclasses import dataclass
import random

pygame.init()


ROWS = 20
COLS = 10
WIDTH = 400
SPACE = WIDTH // COLS
HEIGHT = SPACE * ROWS
BG_COLOR = "black"
FPS = 30
SPEED = 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()


pieces = [pygame.transform.scale(pygame.image.load(
    f"./assets/piece_{i}.png"), (SPACE, SPACE)) for i in range(1, 10)]

TETROMINOES = [
    [0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# User events
SHAPE_DOWN = pygame.USEREVENT+1
pygame.time.set_timer(SHAPE_DOWN, SPEED)


@dataclass
class Tetrominoe():
    shape: list
    row: int = 1
    col: int = 6

    def show(self):
        x = self.col * SPACE
        y = self.row * SPACE
        for i, color in enumerate(self.shape):
            if color > 0:
                x, y =  ((i % 4) + self.col) * SPACE, ((i // 4) + self.row) * SPACE
                win.blit(pieces[color], (x, y))
    
    def move(self, delta_row, delta_col):
        self.row += delta_row
        self.col += delta_col

    def rotate(self):
        shape_copy = self.shape.copy()
        for n, color in enumerate(shape_copy):
            r = n // 4
            c = n % 4
            self.shape[(2-c)*4+r] = color


def draw(win, grid, shape):
    clock.tick(FPS)

    # draw background
    win.fill(BG_COLOR)

    # draw main shape that is falling
    shape.show()

    # draw grid
    for i, color in enumerate(grid):
        if color > 0:
            x, y = (i % COLS) * SPACE, (i // COLS) * SPACE
            win.blit(pieces[color], (x, y))
    
    pygame.display.update()


def run():
    running = True
    
    grid = [0] * WIDTH * HEIGHT
    shape = Tetrominoe(random.choice(TETROMINOES))

    while running:
        # Game Logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SHAPE_DOWN:
                shape.move(1, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    shape.move(0, 1)
                if event.key == pygame.K_LCTRL:
                    shape.rotate()
        
        draw(win, grid, shape)

    pygame.quit()


run()
