# Gold Experience - Discord bot
# Copyright (C) 2019 Giovata
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.

# modules/fun/notcmd/minesweeper.py

import os
import random

emoji = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", "💣"]

def file_output(output_file, text):
    with open(output_file, "w") as f:
        f.write(text)

def count_adjacent(board, y, x, rows, columns):
    #218
    #3 7
    #456
    count = 0

    #1
    if y == 0:
        pass
    elif board[y-1][x] == -1:
        count += 1 
    #2
    if y == 0 or x == 0:
        pass
    elif board[y-1][x-1] == -1:
        count += 1
    #3
    if x == 0:
        pass
    elif board[y][x-1] == -1:
        count += 1
    #4
    if y == rows-1 or x == 0:
        pass
    elif board[y+1][x-1] == -1:
        count += 1
    #5
    if y == rows-1:
        pass
    elif board[y+1][x] == -1:
        count += 1
    #6
    if y == rows-1 or x == columns-1:
        pass
    elif board[y+1][x+1] == -1:
        count += 1
    #7
    if x == columns-1:
        pass
    elif board[y][x+1] == -1:
        count += 1
    #8
    if y == 0 or x == columns-1:
        pass
    elif board[y-1][x+1] == -1:
        count += 1

    return count

def discordify(board, columns, rows):
    text = "​\n"
    for row in range(rows):
        for column in range(columns):
            text += f"||{emoji[board[row][column]]}||"
        text += "\n"
    return text

def generate(rows, columns, bombs):
    board = []
    for row in range(0, rows):
        row_array = []
        for column in range(0, columns):
            row_array.append(0)
        board.append(row_array)

    for bomb in range(0, bombs):
        bomb_x = random.randint(0, columns-1)
        bomb_y = random.randint(0, rows-1)
        while board[bomb_y][bomb_x] != 0:
            bomb_x = random.randint(0, columns-1)
            bomb_y = random.randint(0, rows-1)
        board[bomb_y][bomb_x] = -1

    for row in range(0, rows):
        for column in range(0, columns):
            if board[row][column] == 0:
                board[row][column] = count_adjacent(board, row, column, rows, columns)

    output = discordify(board, columns, rows)
    if len(output) >= 1998:
        output = generate(rows, columns, bombs)
        if len(output) >= 1998:
            output = generate(rows, columns, bombs)
            if len(output) >= 1998:
                return "Unable to generate. Please specify a smaller board size."
    return output

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    output_file = path + "/minesweeper.txt"

    rows = int(input("Rows: "))
    columns = int(input("Columns: "))
    bombs = int(input("Bombs: "))
    board = generate(rows, columns, bombs)
    file_output(output_file, board)
    x = input(board)

