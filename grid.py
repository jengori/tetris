class Grid:
    def __init__(self, filled_positions):
        self.grid = [["black" for _ in range(10)] for _ in range(20)]

        for i in range(20):
            for j in range(10):
                if (i, j) in filled_positions:
                    self.grid[i][j] = filled_positions[(i, j)]
