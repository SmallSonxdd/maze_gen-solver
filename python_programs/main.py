from graphics import *

def main():
    win = Window(800, 600)
    num_cols = 20
    num_rows = 15
    m1 = Maze(0, 0, num_rows, num_cols, 40, 40, win) 
    m1.solve()
    win.wait_for_close()

main()