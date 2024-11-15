from graphics import Window, Point, Line

def main():
    win = Window(800, 600)
    red_line = Line(Point(16,34),Point(700,144))
    win.draw_line(red_line, 'red')
    black_line = Line(Point(400, 400), Point(400, 20))
    win.draw_line(black_line, 'black')
    colorless_line = Line(Point(333, 333), Point(666, 111))
    win.draw_line(colorless_line)
    win.wait_for_close()

main()