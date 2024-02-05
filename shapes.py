class Shape:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.positions = []
        self.position_num = 0
        self.color = None
        self.landed = False

    def move_down(self, filled_spaces):
        self.y += 1
        if not self.is_valid_place(filled_spaces):
            self.y -= 1
            self.landed = True

    def move_left(self, filled_spaces):
        self.x -= 1
        if not self.is_valid_place(filled_spaces):
            self.x += 1

    def move_right(self, filled_spaces):
        self.x += 1
        if not self.is_valid_place(filled_spaces):
            self.x -= 1

    def rotate_left(self, filled_spaces):
        self.position_num = (self.position_num - 1) % len(self.positions)
        if not self.is_valid_place(filled_spaces):
            self.position_num = (self.position_num + 1) % len(self.positions)

    def rotate_right(self, filled_spaces):
        self.position_num = (self.position_num + 1) % len(self.positions)
        if not self.is_valid_place(filled_spaces):
            self.position_num = (self.position_num - 1) % len(self.positions)

    def drop(self, filled_spaces):
        while self.is_valid_place(filled_spaces):
            self.y += 1
        self.y -= 1

    def place(self, grid):
        for i in range(4):
            for j in range(4):
                if self.positions[self.position_num][i][j] == "#":
                    grid.grid[i-1+self.y][j+3+self.x] = self.color

    def is_valid_place(self, filled_spaces):
        if self.out_of_bounds():
            return False
        for i in range(4):
            for j in range(4):
                if self.positions[self.position_num][i][j] == "#":
                    if (i-1+self.y, j+3+self.x) in filled_spaces:
                        return False

        return True

    def out_of_bounds(self):
        for i in range(4):
            for j in range(4):
                if self.positions[self.position_num][i][j] == "#":
                    if i-1+self.y < 0 or j+3+self.x < 0 or i-1+self.y > 19 or j+3+self.x > 9:
                        return True
        return False


class OShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "yellow"
        self.positions = [['....',
                           '.##.',
                           '.##.',
                           '....']]


class IShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "cyan"
        self.positions = [['....',
                           '####',
                           '....',
                           '....'],
                          ['..#.',
                           '..#.',
                           '..#.',
                           '..#.']]


class JShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "blue"
        self.positions = [['....',
                           '#...',
                           '###.',
                           '....'],
                          ['....',
                           '.##.',
                           '.#..',
                           '.#..'],
                          ['....',
                           '....',
                           '###.',
                           '..#.'],
                          ['....',
                           '.#..',
                           '.#..',
                           '##..']]


class LShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "orange"
        self.positions = [['....',
                           '..#.',
                           '###.',
                           '....'],
                          ['....',
                           '.#..',
                           '.#..',
                           '.##.'],
                          ['....',
                           '....',
                           '###.',
                           '#...'],
                          ['....',
                           '##..',
                           '.#..',
                           '.#..']]


class SShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "red"
        self.positions = [['....',
                           '.##..',
                           '##...',
                           '.....'],
                          ['.#..',
                           '.##.',
                           '..#.',
                           '....']]


class ZShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "green"
        self.positions = [['....',
                           '##..',
                           '.##.',
                           '....'],
                          ['.#..',
                           '##..',
                           '#...',
                           '....']]


class TShape(Shape):
    def __init__(self):
        super().__init__()

        self.color = "purple"
        self.positions = [['....',
                           '.#..',
                           '###.',
                           '....'],
                          ['....',
                           '.#..',
                           '.##.',
                           '.#..'],
                          ['....',
                           '....',
                           '###.',
                           '.#..'],
                          ['....',
                           '.#..',
                           '##..',
                           '.#..']]

