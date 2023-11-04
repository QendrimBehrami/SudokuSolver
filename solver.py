# Tilemap flag states
EMPTY = 0
ORIGINAL_PUZZLE = 1
SELECTED = 2
MODIFIED = 3

import pygame


def solve(sudoku_values, sudoku_flags):
    return solveCell(0, 0, sudoku_values, sudoku_flags)


def solveCell(row, column, sudoku_values, sudoku_flags) -> bool:
    # End of the board
    if row == 8 and column == 8:
        return checkRow(row, sudoku_values)

    nextRow = row if column < 8 else row + 1
    nextColumn = column + 1 if column < 8 else 0

    if sudoku_flags[row, column] == ORIGINAL_PUZZLE:
        return solveCell(nextRow, nextColumn, sudoku_values, sudoku_flags)
    else:
        i = 1
        while i <= 9:
            pygame.time.delay(1)
            sudoku_values[row][column] = i
            sudoku_flags[row][column] = MODIFIED
            if (
                checkRow(row, sudoku_values)
                and checkColumn(column, sudoku_values)
                and checkGrid(row, column, sudoku_values)
                and solveCell(nextRow, nextColumn, sudoku_values, sudoku_flags)
            ):
                return True
            else:
                i += 1
        # One of the previous answers must have been wrong
        sudoku_values[row][column] = 0

        return False


def checkRow(rowIndex, sudoku_values):
    seen_numbers = set()
    for entry in sudoku_values[rowIndex]:
        if entry == 0:
            continue
        if entry in seen_numbers:
            return False
        else:
            seen_numbers.add(entry)
    return True


def checkColumn(columnIndex, sudoku_values):
    seen_numbers = set()
    for i in range(0, 9):
        entry = sudoku_values[i][columnIndex]
        if entry == 0:
            continue
        if entry in seen_numbers:
            return False
        else:
            seen_numbers.add(entry)
    return True


def checkGrid(rowIndex, columnIndex, sudoku_values):
    gridRow = rowIndex // 3
    gridColumn = columnIndex // 3
    seen_numbers = set()
    for i in range(0, 3):
        for j in range(0, 3):
            entry = sudoku_values[gridRow * 3 + i][gridColumn * 3 + j]

            if entry == 0:
                continue
            if entry in seen_numbers:
                return False
            else:
                seen_numbers.add(entry)
    return True
