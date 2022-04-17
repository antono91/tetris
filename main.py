from re import S
import pygame
from dataclasses import dataclass

pygame.init()

ROWS = 20
COLS = 10
WIDTH = 400
SPACE = WIDTH // COLS
HEIGHT = SPACE * ROWS
BG_COLOR = "black"

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")


pieces = [pygame.transform.scale(pygame.image.load(
    f"./assets/piece_{i}.png"), (SPACE, SPACE)) for i in range(1, 10)]

TETROMINOES = [
    [0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 4, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

grid = [0] * WIDTH * HEIGHT


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

t = Tetrominoe(TETROMINOES[0])

def draw(win):
    win.fill(BG_COLOR)
    t.show()
    for i, color in enumerate(grid):
        if color > 0:
            x, y = (i % COLS) * SPACE, (i // COLS) * SPACE
            win.blit(pieces[color], (x, y))
    pygame.display.update()


def run():
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw(win)

    pygame.quit()


run()
