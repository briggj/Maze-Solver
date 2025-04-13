from tkinter import Tk, BOTH, Canvas
import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2, fill_color="black"):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            line.draw(self._win._Window__canvas, fill_color)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            line.draw(self._win._Window__canvas, "white")

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            line.draw(self._win._Window__canvas, fill_color)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            line.draw(self._win._Window__canvas, "white")

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            line.draw(self._win._Window__canvas, fill_color)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            line.draw(self._win._Window__canvas, "white")

        if self.has_bottom_wall:
            line = Line(Point(x2, y2), Point(x1, y2))
            line.draw(self._win._Window__canvas, fill_color)
        else:
            line = Line(Point(x2, y2), Point(x1, y2))
            line.draw(self._win._Window__canvas, "white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        x_mid1 = (self._x1 + self._x2) / 2
        y_mid1 = (self._y1 + self._y2) / 2
        x_mid2 = (to_cell._x1 + to_cell._x2) / 2
        y_mid2 = (to_cell._y1 + to_cell._y2) / 2

        fill_color = "red"
        if undo:
            fill_color = "gray"

        line = Line(Point(x_mid1, y_mid1), Point(x_mid2, y_mid2))
        line.draw(self._win._Window__canvas, fill_color)

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                col_cells.append(cell)
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].draw(self._x1, self._y1, self._x1 + self._cell_size_x, self._y1 + self._cell_size_y)

        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        x_exit = self._x1 + (self._num_cols - 1) * self._cell_size_x
        y_exit = self._y1 + (self._num_rows - 1) * self._cell_size_y
        self._cells[self._num_cols - 1][self._num_rows - 1].draw(x_exit, y_exit, x_exit + self._cell_size_x, y_exit + self._cell_size_y)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_directions = []

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append(("L", i - 1, j))

            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append(("R", i + 1, j))

            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append(("U", i, j - 1))

            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append(("D", i, j + 1))

            if not possible_directions:
                self._draw_cell(i, j)
                return

            direction, next_i, next_j = random.choice(possible_directions)

            if direction == "L":
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][j].has_right_wall = False
            elif direction == "R":
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][j].has_left_wall = False
            elif direction == "U":
                self._cells[i][j].has_top_wall = False
                self._cells[i][next_j].has_bottom_wall = False
            elif direction == "D":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][next_j].has_top_wall = False

            self._draw_cell(i, j)
            self._draw_cell(next_i, next_j)
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # left
        if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        # right
        if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        # up
        if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # down
        if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        return False


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("My Graphical Window")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

if __name__ == "__main__":
    win = Window(800, 600)
    maze = Maze(50, 50, 10, 10, 50, 50, win, 0)
    maze.solve()
    win.wait_for_close()