import pygame
import numpy as np
import threading
import time
import solver

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (640, 640)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sudoku Solver")


# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


# Tilemap flag states
EMPTY = 0
ORIGINAL_PUZZLE = 1
SELECTED = 2
MODIFIED = 3

# Initialize a 9x9 Sudoku grid with zeros (representing empty cells)
grid_size = 9
sudoku_values = np.zeros((grid_size, grid_size), dtype=int)
sudoku_flags = np.zeros((grid_size, grid_size), dtype=int)  # Integer array for flags

# Set an example Sudoku puzzle (0 represents empty cells)
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

# Fill the Sudoku grid with the example puzzle values and set flags
for i in range(grid_size):
    for j in range(grid_size):
        value = example_puzzle[i][j]
        if value != 0:
            sudoku_values[i][j] = value
            sudoku_flags[i][
                j
            ] = ORIGINAL_PUZZLE  # Set the flag for original puzzle values

selected_tile = (-1, -1)


def get_tile_size():
    return window.get_width() / (grid_size + 1)


def draw_grid():
    tile_size = get_tile_size()

    for i in range(0, (grid_size + 1)):
        thickness = 4 if i % 3 == 0 else 1

        # Vertical Lines
        pygame.draw.line(
            window,
            BLACK,
            (tile_size / 2 + tile_size * i, tile_size / 2),
            (tile_size / 2 + tile_size * i, tile_size / 2 + grid_size * tile_size),
            thickness,
        )

        # Horizontal Lines
        pygame.draw.line(
            window,
            BLACK,
            (
                tile_size / 2,
                tile_size / 2 + tile_size * i,
            ),
            (
                tile_size / 2 + grid_size * tile_size,
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

    for i in range(0, grid_size):
        for j in range(0, grid_size):
            flag = sudoku_flags[i][j]
            if flag == EMPTY:
                continue
            text = str(sudoku_values[i][j])

            text_color = BLACK

            if flag == SELECTED:
                text_color = BLACK
                text = "_"

            elif flag == MODIFIED:
                if text == "0":
                    continue
                text_color = GREEN

            rendered_text = font.render(text, anti_aliasing, text_color, WHITE)

            window.blit(
                rendered_text, (tile_size * (j + 0.5) + x, tile_size * (i + 0.5) + y)
            )


def select_tile(pos):
    mx, my = pos
    tile_size = get_tile_size()
    global selected_tile
    tx = int((mx - tile_size // 2) // tile_size)
    ty = int((my - tile_size // 2) // tile_size)

    old_x, old_y = selected_tile

    unselect_tile(old_x, old_y)

    # Setup new selection
    sudoku_flags[ty][tx] = SELECTED
    selected_tile = (ty, tx)


def unselect_tile(sx, sy):
    global selected_tile
    if sx != -1 and sy != -1:
        if sudoku_values[sx][sy] == 0:
            sudoku_flags[sx][sy] = EMPTY
        else:
            sudoku_flags[sx][sy] = ORIGINAL_PUZZLE
    selected_tile = (-1, -1)


def solve_sudoku_thread():
    global sudoku_flags, sudoku_values
    solved = solver.solve(sudoku_values, sudoku_flags)
    if solved:
        print("Sudoku was solved.")
    else:
        print("Sudoku cannot be solved.")


def process_keys(keys):
    global selected_tile
    sx, sy = selected_tile

    # Unselect
    if keys[pygame.K_ESCAPE]:
        unselect_tile(sx, sy)

    # Modify board
    for key in range(pygame.K_0, pygame.K_9 + 1):
        if keys[key] and sx != -1 and sy != -1:
            sudoku_values[sx, sy] = key - pygame.K_1 + 1
            sudoku_flags[sx, sy] = ORIGINAL_PUZZLE
            unselect_tile(sx, sy)
            break

    # Start Solving
    if keys[pygame.K_s]:
        # solved = solver.solve(sudoku_values, sudoku_flags)
        # if solved:
        #     print("Success!")
        # else:
        #     print("Failure!")
        sudoku_solver_thread = threading.Thread(target=solve_sudoku_thread)
        sudoku_solver_thread.start()

    # Clear board
    if keys[pygame.K_c]:
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                flag = sudoku_flags[i, j]
                if flag == MODIFIED:
                    sudoku_flags[i][j] = EMPTY
                    sudoku_values[i][j] = 0


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            select_tile(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            process_keys(pygame.key.get_pressed())

    # Fill the background
    window.fill(WHITE)

    draw_grid()

    # Update the display
    pygame.display.update()

pygame.quit()
