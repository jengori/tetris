from shapes import *
import random
from grid import Grid

shapes = [OShape, IShape, JShape, LShape, SShape, ZShape, TShape]


class Game:
    def __init__(self):
        self.score = 0
        self.lines = 0
        self.level = 1
        self.active_shape = random.choice(shapes)()
        self.next_shape = random.choice(shapes)()
        self.filled_spaces = {}
        self.counter = 0
        self.speed = 2
        self.paused = False
        self.grid = Grid(self.filled_spaces)
        self.game_over = False

    def play(self):
        if not self.paused and not self.game_over:
            self.counter += self.speed

        self.grid = Grid(self.filled_spaces)
        if self.counter >= 60:
            self.active_shape.move_down(self.filled_spaces)
            self.counter = 0
        self.active_shape.place(self.grid)
        self.handle_complete_rows()

        if self.active_shape.landed:
            self.update_filled_spaces()
            self.active_shape = self.next_shape
            self.next_shape = random.choice(shapes)()
            if not self.active_shape.is_valid_place(self.filled_spaces):
                self.game_over = True

    def handle_complete_rows(self):
        num_completed_rows = 0
        for row_num in range(20):
            row_complete = True
            for col_num in range(10):
                if (row_num, col_num) not in self.filled_spaces:
                    row_complete = False
            if row_complete:
                num_completed_rows += 1
                updated_filled_spaces = {}
                for key, value in self.filled_spaces.items():
                    if key[0] > row_num:
                        updated_filled_spaces[(key[0], key[1])] = value
                    elif key[0] < row_num:
                        updated_filled_spaces[(key[0]+1, key[1])] = value
                self.filled_spaces = updated_filled_spaces
                self.score += 10 * self.level * num_completed_rows
                self.lines += 1
                if self.lines % 10 == 0:
                    self.level_up()

    def level_up(self):
        self.level += 1
        if self.level <= 10:
            self.speed += 0.5
        elif self.level <= 20:
            self.speed += 0.25

    def update_filled_spaces(self):
        for i in range(4):
            for j in range(4):
                if self.active_shape.positions[self.active_shape.position_num][i][j] == "#":
                    self.filled_spaces[(i-1+self.active_shape.y, j+3+self.active_shape.x)] = self.active_shape.color

