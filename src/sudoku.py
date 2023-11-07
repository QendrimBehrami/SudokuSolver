import pygame
import numpy as np
import threading
import solver
from enum import Enum

# An example Sudoku puzzle (0 represents empty cells)
example_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


# Tilemap flag states
class Flag(Enum):
    EMPTY = 0
    ORIGINAL_PUZZLE = 1
    SELECTED = 2
    MODIFIED = 3


Colors = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "BLACK": (0, 0, 0),
    "GREEN": (0, 255, 0),
}


class Sudoku:
    def __init__(self, size=640) -> None:
        # Initialize Pygame
        pygame.init()

        self.window_size = (size, size)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Sudoku Solver")

        self.sudoku_values = np.zeros(
            (9, 9), dtype=int
        )  # Numbers in each cell (0 = empty)
        self.sudoku_flags = [
            [Flag.EMPTY for _ in range(9)] for _ in range(9)
        ]  # Integer array for flags

        # Fill the Sudoku grid with the example puzzle values and set flags
        for i in range(9):
            for j in range(9):
                value = example_puzzle[i][j]
                if value != 0:
                    self.sudoku_values[i][j] = value
                    self.sudoku_flags[i][
                        j
                    ] = Flag.ORIGINAL_PUZZLE  # Set the flag for original puzzle values

        self.selected_tile = (
            -1,
            -1,
        )  # Currently selected tile, (-1,-1) represents no selection

    def get_tile_size(self):
        return self.window.get_width() / 10

    def draw_grid(self):
        self.window.fill(Colors["WHITE"])  # Clear window
        tile_size = self.get_tile_size()

        for i in range(0, 10):
            thickness = 4 if i % 3 == 0 else 1

            # Vertical Lines
            pygame.draw.line(
                self.window,
                Colors["BLACK"],
                (tile_size / 2 + tile_size * i, tile_size / 2),
                (tile_size / 2 + tile_size * i, tile_size / 2 + 9 * tile_size),
                thickness,
            )

            # Horizontal Lines
            pygame.draw.line(
                self.window,
                Colors["BLACK"],
                (
                    tile_size / 2,
                    tile_size / 2 + tile_size * i,
                ),
                (
                    tile_size / 2 + 9 * tile_size,
                    tile_size / 2 + tile_size * i,
                ),
                thickness,
            )

        # Draw numbers

        font_size = 48
        font = pygame.font.Font(None, font_size)
        anti_aliasing = True
        text_width, text_height = font.size("0")
        x = (tile_size - text_width) // 2
        y = (tile_size - text_height) // 2

        for i in range(0, 9):
            for j in range(0, 9):
                flag = self.sudoku_flags[i][j]
                if flag == Flag.EMPTY:
                    continue
                text = str(self.sudoku_values[i][j])

                text_color = Colors["BLACK"]

                if flag == Flag.SELECTED:
                    text_color = Colors["BLACK"]
                    text = "_"

                elif flag == Flag.MODIFIED:
                    if text == "0":
                        continue
                    text_color = Colors["GREEN"]

                rendered_text = font.render(
                    text, anti_aliasing, text_color, Colors["WHITE"]
                )

                self.window.blit(
                    rendered_text,
                    (tile_size * (j + 0.5) + x, tile_size * (i + 0.5) + y),
                )
        # Update the display
        pygame.display.update()

    def select_tile(self, pos):
        mx, my = pos
        tile_size = self.get_tile_size()
        tx = int((mx - tile_size // 2) // tile_size)
        ty = int((my - tile_size // 2) // tile_size)

        old_x, old_y = self.selected_tile

        self.unselect_tile(old_x, old_y)

        # Setup new selection
        self.sudoku_flags[ty][tx] = Flag.SELECTED
        self.selected_tile = (ty, tx)

    def unselect_tile(self, sx, sy):
        if sx != -1 and sy != -1:
            if self.sudoku_values[sx][sy] == 0:
                self.sudoku_flags[sx][sy] = Flag.EMPTY
            else:
                self.sudoku_flags[sx][sy] = Flag.ORIGINAL_PUZZLE
        self.selected_tile = (-1, -1)

    def solve_sudoku_thread(self):
        # global sudoku_flags, sudoku_values
        solved = solver.solve(self)
        if solved:
            print("Sudoku was solved.")
        else:
            print("Sudoku cannot be solved.")

    def process_keys(self, keys):
        sx, sy = self.selected_tile

        # Unselect
        if keys[pygame.K_ESCAPE]:
            self.unselect_tile(sx, sy)

        # Modify board
        for key in range(pygame.K_0, pygame.K_9 + 1):
            if keys[key] and sx != -1 and sy != -1:
                self.sudoku_values[sx, sy] = key - pygame.K_1 + 1
                self.sudoku_flags[sx][sy] = Flag.ORIGINAL_PUZZLE
                self.unselect_tile(sx, sy)
                break

        # Start Solving
        if keys[pygame.K_s]:
            # solved = solver.solve(sudoku_values, sudoku_flags)
            # if solved:
            #     print("Success!")
            # else:
            #     print("Failure!")
            sudoku_solver_thread = threading.Thread(target=self.solve_sudoku_thread)
            sudoku_solver_thread.start()

        # Clear board
        if keys[pygame.K_c]:
            for i in range(0, 9):
                for j in range(0, 9):
                    flag = self.sudoku_flags[i, j]
                    if flag == Flag.MODIFIED:
                        self.sudoku_flags[i][j] = Flag.EMPTY
                        self.sudoku_values[i][j] = 0
