from graphics import Window, Point, Line, Cell

def main():
    win = Window(800, 600)
    cell_one = Cell(Point(24, 24), Point(36, 36), win)
    cell_one.draw()
    cell_two = Cell(Point(60, 60), Point(77, 77), win)
    cell_two.has_left_wall = False
    cell_two.has_bottom_wall = False
    cell_two.has_right_wall = False
    cell_two.draw()
    cell_three = Cell(Point(28,28), Point(66, 66), win)
    cell_three.has_left_wall = False
    cell_three.draw()
    win.wait_for_close()

main()