from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title('Maze Solver')
        self.__canvas = Canvas(self.__root, bg='white', height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running is True:
            self.redraw()
        print('go agane')
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color='black'):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        #x and y are horizontal and vertical coordinates respectively
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        if not isinstance(point1, Point) and not isinstance(point2, Point):
            raise TypeError("one of those ain't an instance of Point class, buckaroo")
        self.point1 = point1
        self.point2 = point2
    
    def draw(self, canvas, fill_color='black'):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, top_left, bottom_right, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = top_left.x
        self._x2 = bottom_right.x
        self._y1 = top_left.y
        self._y2 = bottom_right.y
        self._win = window

    def draw(self):
        if self.has_left_wall:
            print(f'Cell {self} has left wall biatch')
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line)
        if self.has_bottom_wall:
            print(f'Cell {self} has bottom wall biatch')
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line)
        if self.has_right_wall:
            print(f'Cell {self} has right wall biatch')
            line = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
            self._win.draw_line(line)
        if self.has_top_wall:
            print(f'Cell {self} has top wall biatch')
            line = Line(Point(self._x2, self._y1), Point(self._x1, self._y1))
            self._win.draw_line(line)

    def draw_move(self, to_cell, undo=False):
        if undo is False:
            color = 'red'
        else:
            color = 'gray'
        center_from = Point((self._x1 + self._x2)/2, (self._y1 + self._y2)//2)
        center_to = Point((to_cell._x1 + to_cell._x2)/2, (to_cell._y1 + to_cell._y2)//2)
        line = Line(center_from, center_to)
        self._win.draw_line(line, fill_color=color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._create_cells()
    
    def _create_cells(self):
        self._cells = []
        x = self.x1
        y = self.y1
        for column_index in range(self.num_cols):
            column_of_cells = []
            helper_x = x + self.cell_size_x
            for row_index in range(self.num_rows):
                helper_y = y + self.cell_size_y
                cell = Cell(Point(x, y), Point(helper_x, helper_y), self.win)
                column_of_cells.append(cell)
                y = helper_y
            self._cells.append(column_of_cells)
            x = helper_x
            y = self.y1
        for column in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(row, column)
    
    def _draw_cell(self, i, j):
        cell = self._cells[j][i]
        cell.draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)
