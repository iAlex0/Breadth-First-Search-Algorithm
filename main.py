import curses
from curses import wrapper
import queue
import time
import sys


maze = [    
    ["#", "#", "#", "#", "O", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[], message=None):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    GREEN = curses.color_pair(3)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, "X", RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)

    if message:
        if message == "Path found":
            stdscr.addstr(len(maze)+1, 0, message, GREEN)
        elif message == "Path not found":
            stdscr.addstr(len(maze)+1, 0, message, RED)

    stdscr.refresh()


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return (i, j)
    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        print_maze(maze, stdscr, path)
        time.sleep(0.2)

        if maze[row][col] == end:
            print_maze(maze, stdscr, path, message="Path found")
            return path

        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)

    print_maze(maze, stdscr, message="Path not found")
    return None


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    path = find_path(maze, stdscr)

    if path:
        stdscr.clear()
        print_maze(maze, stdscr, path)
        stdscr.addstr(len(maze) + 1, 0, "Path found!", curses.color_pair(3))
    else:
        stdscr.addstr(len(maze) + 1, 0, "Path not found.", curses.color_pair(2))

    stdscr.refresh()
    time.sleep(2)




if __name__ == "__main__":
    wrapper(main)