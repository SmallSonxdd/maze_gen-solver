from tkinter import Tk, BOTH, Canvas
import time
import random

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
        self.visited = False
        self.location_in_maze = [0, 0]

    def draw(self):
        if self._win is None:
            return
        line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        if self.has_left_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, 'white')
        line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        if self.has_bottom_wall:            
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, 'white')
        line = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
        if self.has_right_wall:            
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, 'white')
        line = Line(Point(self._x2, self._y1), Point(self._x1, self._y1))
        if self.has_top_wall:            
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, 'white')
        line = None

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
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed != None:
            self.seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
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
                cell.location_in_maze = [row_index, column_index]
                column_of_cells.append(cell)
                y = helper_y
            self._cells.append(column_of_cells)
            x = helper_x
            y = self.y1
        for column in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cell(row, column)
    
    def _draw_cell(self, i, j):
        if self.win is None:
            return
        if i > self.num_rows or j > self.num_cols:
            return
        cell = self._cells[j][i]
        cell.draw()
        self._animate()
    
    def _animate(self):
        self.win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        cell_entrance = self._cells[0][0]
        cell_entrance.has_top_wall = False
        self._draw_cell(0, 0)
        cell_exit = self._cells[self.num_cols-1][self.num_rows-1]
        cell_exit.has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)
    
    def _break_walls_r(self, i, j):
        current_cell = self._cells[j][i]
        current_cell.visited = True
        while True:
            adjacent_cells = {}
            if j > 0:
                cell_left = self._cells[j-1][i]
                if not cell_left.visited:
                    adjacent_cells['cell_left'] = cell_left
            if i > 0:
                cell_top = self._cells[j][i - 1]
                if not cell_top.visited:
                    adjacent_cells['cell_top'] = cell_top
            if self.num_cols > j + 1:
                cell_right = self._cells[j + 1][i]
                if not cell_right.visited:
                    adjacent_cells['cell_right'] = cell_right
            if self.num_rows > i + 1:
                cell_bottom = self._cells[j][i + 1]
                if not cell_bottom.visited:
                    adjacent_cells['cell_bottom'] = cell_bottom
            
            if adjacent_cells == {}:
                self._draw_cell(i, j)
                return
            random_seed = random.randrange(len(adjacent_cells))
            random_cell_key = list(adjacent_cells.keys())[random_seed]
            random_cell_value = adjacent_cells[random_cell_key]
            if random_cell_key == 'cell_left':
                current_cell.has_left_wall = False
                random_cell_value.has_right_wall = False
                self._break_walls_r(i, j - 1)
            if random_cell_key == 'cell_top':
                current_cell.has_top_wall = False
                random_cell_value.has_bottom_wall = False
                self._break_walls_r(i - 1, j)
            if random_cell_key == 'cell_right':
                current_cell.has_right_wall = False
                random_cell_value.has_left_wall = False
                self._break_walls_r(i, j + 1)
            if random_cell_key == 'cell_bottom':
                current_cell.has_bottom_wall = False
                random_cell_value.has_top_wall = False
                self._break_walls_r(i + 1, j)

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False
    
    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[j][i]
        current_cell.visited = True
        if current_cell == self._cells[self.num_cols - 1][self.num_rows - 1]:
            return True
        
        #left
        if j > 0 and not self._cells[j-1][i].visited and (current_cell.has_left_wall == False and self._cells[j-1][i].has_right_wall == False):
            current_cell.draw_move(self._cells[j-1][i])
            result = self._solve_r(i, j-1)
            if result:
                return True
            self._cells[j-1][i].draw_move(current_cell, undo=True)
        #top
        if i > 0 and not self._cells[j][i-1].visited and (current_cell.has_top_wall == False and self._cells[j][i-1].has_bottom_wall == False):
            current_cell.draw_move(self._cells[j][i-1])
            result = self._solve_r(i-1, j)
            if result:
                return True
            self._cells[j][i-1].draw_move(current_cell, undo=True)
        #right
        if self.num_cols > j + 1 and not self._cells[j + 1][i].visited and (current_cell.has_right_wall == False and self._cells[j + 1][i].has_left_wall == False):
            current_cell.draw_move(self._cells[j + 1][i])
            result = self._solve_r(i, j+1)
            if result:
                return True
            self._cells[j + 1][i].draw_move(current_cell, undo=True)
        #bottom
        if self.num_rows > i + 1 and not self._cells[j][i + 1].visited and (current_cell.has_bottom_wall == False and self._cells[j][i + 1].has_top_wall == False):
            current_cell.draw_move(self._cells[j][i + 1])
            result = self._solve_r(i+1, j)
            if result:
                return True
            self._cells[j][i + 1].draw_move(current_cell, undo=True)
        return False

