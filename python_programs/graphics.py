from tkinter import Tk, BOTH, Canvas

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

    def draw_line(self, line, fill_color='purple'):
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
    
    def draw(self, canvas, fill_color='purple'):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
