from graphics import Window, Point, Line, Cell

def main():
    win = Window(800, 600)
    cell_one = Cell(Point(40, 40), Point(80, 80), win)
    cell_one.draw()
    cell_two = Cell(Point(400, 40), Point(440, 160), win)
    cell_two.draw()
    cell_one.draw_move(cell_two, undo=False)
    cell_three = Cell(Point(200,200), Point(500, 500), win)
    cell_three.draw()
    cell_two.draw_move(cell_three)
    cell_three.draw_move(cell_one, undo='gibigaba')
    win.wait_for_close()

main()