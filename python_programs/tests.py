import unittest
from graphics import *  # only import what you need

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)  # Note: win=None here
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        
    
    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_break_walls(self):
    # Create a small 2x2 maze with seed 0 for reproducibility
        maze = Maze(0, 0, 2, 2, 10, 10, seed=5)
    
    # Call break walls on the starting cell (0,0)
        maze._break_walls_r(0, 0)
    
    # Test 1: Check if starting cell was visited
        assert maze._cells[0][0].visited == True, "Starting cell should be visited"
    
    # Test 2: Check if all cells were visited
        all_visited = all(cell.visited for column in maze._cells for cell in column)
        assert all_visited == True, "All cells should be visited"
    
    # Test 3: Check if there's at least one broken wall
        has_broken_wall = False
        for column in maze._cells:
            for cell in column:
                if (not cell.has_left_wall or not cell.has_right_wall or 
                    not cell.has_top_wall or not cell.has_bottom_wall):
                    has_broken_wall = True
                    break
        assert has_broken_wall == True, "Should have at least one broken wall"
    
    # Test 4: Check if walls are broken in pairs
    # If left wall of (0,0) is broken, right wall of (-1,0) should be broken
        if not maze._cells[0][0].has_left_wall and j > 0:
            assert not maze._cells[j-1][0].has_right_wall


if __name__ == "__main__":
    unittest.main()