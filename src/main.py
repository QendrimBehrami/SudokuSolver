import pygame
import numpy as np
import threading
import solver
from sudoku import Sudoku


def main():
    # Main game loop
    pygame.init()
    sudoku = Sudoku()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sudoku.select_tile(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                sudoku.process_keys(pygame.key.get_pressed())

        sudoku.draw_grid()

    pygame.quit()


if __name__ == "__main__":
    main()
