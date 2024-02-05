import pygame
from constants import *
from game import Game
from shapes import *

pygame.init()

large_text = pygame.font.SysFont(FONT, size=50)
medium_text = pygame.font.SysFont(FONT, size=30)
small_text = pygame.font.SysFont(FONT, size=20)
tiny_text = pygame.font.SysFont(FONT, size=14)


class Tetris:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.help_screen = False
        self.game_over = False
        self.game = None
        self.clock = pygame.time.Clock()
        self.mouse_pos = pygame.mouse.get_pos()

        with open("high_score.txt") as f:
            try:
                self.high_score = int(f.read())
            except ValueError:
                self.high_score = 0

        self.main_loop()

    def main_loop(self):

        while True:
            self.check_events()
            self.draw_window()
            self.mouse_pos = pygame.mouse.get_pos()
            self.clock.tick(FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game and not self.help_screen:
                # if help button is clicked on title screen
                if 350 < self.mouse_pos[0] < 450 and 245 < self.mouse_pos[1] < 295:
                    self.help_screen = True

                # if play button is clicked on title screen
                elif PLAY_X < self.mouse_pos[0] < PLAY_X+BUTTON_WIDTH and PLAY_Y < self.mouse_pos[1] < PLAY_Y+BUTTON_HEIGHT:
                    self.game = Game()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game and self.help_screen:
                # if back button is clicked on help screen
                if BACK_X < self.mouse_pos[0] < BACK_X+BUTTON_WIDTH and BACK_Y < self.mouse_pos[1] < BACK_Y+BUTTON_HEIGHT:
                    self.help_screen = False

            if event.type == pygame.MOUSEBUTTONDOWN and self.game:
                # if quit button is clicked on game screen
                if QUIT_X < self.mouse_pos[0] < QUIT_X+BUTTON_WIDTH and QUIT_Y < self.mouse_pos[1] < QUIT_Y+BUTTON_HEIGHT:
                    self.game_over = False
                    self.game = None

            if event.type == pygame.MOUSEBUTTONDOWN and self.game and self.game_over:
                # if restart button is clicked on game screen
                if RESTART_X < self.mouse_pos[0] < RESTART_X+BUTTON_HEIGHT and RESTART_Y < self.mouse_pos[1] < RESTART_Y+BUTTON_HEIGHT:
                    self.game_over = False
                    self.game = Game()

            if event.type == pygame.KEYDOWN and self.game:
                # handle game keyboard controls
                if not self.game.paused and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.game.active_shape.move_left(self.game.filled_spaces)
                    if event.key == pygame.K_RIGHT:
                        self.game.active_shape.move_right(self.game.filled_spaces)
                    if event.key == pygame.K_z:
                        self.game.active_shape.rotate_left(self.game.filled_spaces)
                    if event.key == pygame.K_x:
                        self.game.active_shape.rotate_right(self.game.filled_spaces)
                    if event.key == pygame.K_SPACE:
                        self.game.active_shape.drop(self.game.filled_spaces)
                    if event.key == pygame.K_DOWN:
                        self.game.speed += 4
                if event.key == pygame.K_p:
                    if not self.game.paused:
                        self.game.paused = True
                    else:
                        self.game.paused = False

            if event.type == pygame.KEYUP and self.game:
                # handle game keyboard controls
                if event.key == pygame.K_DOWN:
                    self.game.speed -= 4

    def draw_window(self):
        self.window.fill(GRAY)

        if not self.game:

            if not self.help_screen:
                self.draw_title_screen()
            else:
                self.draw_help_screen()

        else:
            if not self.game_over:
                self.game_play_process()
            else:
                self.game_over_process()

        pygame.display.flip()

    def draw_title_screen(self):
        self.display_title()
        self.display_play_button()
        self.display_help_button()
        self.display_high_score()
        self.display_borders()

    def draw_help_screen(self):
        self.display_help_screen_title()
        self.display_instructions()
        self.display_back_button()

    def game_play_process(self):
        self.draw_border()
        self.draw_grid(self.game.grid)
        self.game.play()
        self.display_score()
        self.display_lines()
        self.display_level()
        self.display_next_shape()
        self.display_quit_button()
        self.display_pause_message()
        if self.game.game_over:
            self.game_over = True

    def game_over_process(self):
        self.draw_border()
        self.draw_grid(self.game.grid)
        self.display_score()
        self.display_lines()
        self.display_level()
        self.display_restart_button()
        self.display_quit_button()
        self.update_high_score()
        self.display_game_over_text()

    def display_title(self):
        title_text = large_text.render(TITLE, True, LIGHT_GRAY)
        self.window.blit(title_text, ((WIDTH / 2) - (title_text.get_width() / 2), 155))

    def display_play_button(self):
        self.make_button(PLAY_X, PLAY_Y, "play")

    def display_help_button(self):
        self.make_button(HELP_X, HELP_Y, "help")

    def display_high_score(self):
        high_score_title = small_text.render("HIGH SCORE:", True, LIGHT_GRAY)
        high_score_text = medium_text.render(str(self.high_score), True, LIGHT_GRAY)
        self.window.blit(high_score_title, ((WIDTH / 2) - (high_score_title.get_width() / 2), 355))
        self.window.blit(high_score_text, ((WIDTH / 2) - (high_score_text.get_width() / 2), 380))

    def display_help_screen_title(self):
        start_screen_title = large_text.render("How to Play Tetris", True, LIGHT_GRAY)
        self.window.blit(start_screen_title, ((WIDTH / 2) - (start_screen_title.get_width() / 2), 100))

    def display_back_button(self):
        self.make_button(BACK_X, BACK_Y, "back")

    def display_instructions(self):
        instructions_line_1 = small_text.render("Complete rows to score points!", True, LIGHT_GRAY)
        self.window.blit(instructions_line_1, ((WIDTH * 0.5) - (instructions_line_1.get_width() / 2), 200))
        instructions_line_2 = small_text.render("LEFT ARROW KEY - moves a shape to the left", True, LIGHT_GRAY)
        self.window.blit(instructions_line_2, (60, 260))
        instructions_line_3 = small_text.render("RIGHT ARROW KEY - moves a shape to the right", True, LIGHT_GRAY)
        self.window.blit(instructions_line_3, (60, 290))
        instructions_line_4 = small_text.render("Z - rotates a shape anticlockwise", True, LIGHT_GRAY)
        self.window.blit(instructions_line_4, (60, 320))
        instructions_line_5 = small_text.render("X rotates a shape clockwise", True, LIGHT_GRAY)
        self.window.blit(instructions_line_5, (60, 350))
        instructions_line_6 = small_text.render("DOWN ARROW KEY - speeds up a shape", True, LIGHT_GRAY)
        self.window.blit(instructions_line_6, (60, 380))
        instructions_line_7 = small_text.render("SPACE BAR - drops a shape to the bottom of the grid", True, LIGHT_GRAY)
        self.window.blit(instructions_line_7, (60, 410))
        instructions_line_8 = small_text.render("P - pauses and unpauses the game", True, LIGHT_GRAY)
        self.window.blit(instructions_line_8, (60, 440))

    def draw_border(self):
        pygame.draw.rect(self.window, LIGHT_GRAY, (60, 80, 240, 440))

    def draw_grid(self, grid):
        for i in range(20):
            for j in range(10):
                pygame.draw.rect(self.window, grid.grid[i][j], (80+j*20, 100+i*20, 20, 20))

        for n in range(1, 10):
            pygame.draw.line(self.window, GRAY,
                             (80 + n * 20, 100),
                             (80 + n * 20, 499))
        for n in range(1, 20):
            pygame.draw.line(self.window, GRAY,
                             (80, 100 + n * 20),
                             (279, 100 + n * 20))

    def display_quit_button(self):
        self.make_button(QUIT_X, QUIT_Y, "quit")

    def display_pause_message(self):
        pause_message = tiny_text.render("Press 'P' to pause and unpause the game", True, LIGHT_GRAY)
        self.window.blit(pause_message, (300 - (pause_message.get_width() / 2), 550))

    def display_score(self):
        score_text = medium_text.render(f"Score: {self.game.score}", True, LIGHT_GRAY)
        self.window.blit(score_text, (450 - (score_text.get_width() / 2), 100))

    def display_lines(self):
        lines_text = medium_text.render(f"Lines: {self.game.lines}", True, LIGHT_GRAY)
        self.window.blit(lines_text, (450 - (lines_text.get_width() / 2), 150))

    def display_level(self):
        level_text = medium_text.render(f"Level: {self.game.level}", True, LIGHT_GRAY)
        self.window.blit(level_text, (450 - (level_text.get_width() / 2), 200))

    def draw_shape(self, shape, x, y):
        for i in range(4):
            for j in range(4):
                if shape.positions[shape.position_num][i][j] == "#":
                    pygame.draw.rect(self.window, shape.color, (x+20*j, y+20*i, 20, 20))
                    pygame.draw.line(self.window, BLACK, (x+20*j, y+20*i), (x+20*j, y+20*(i+1)))
                    pygame.draw.line(self.window, BLACK, (x+20*j, y+20*i), (x+20*(j+1), y+20*i))
                    pygame.draw.line(self.window, BLACK, (x+20*(j+1), y+20*i), (x+20*(j+1), y+20*(i+1)))
                    pygame.draw.line(self.window, BLACK, (x+20*j, y+20*(i+1)), (x+20*(j+1), y+20*(i+1)))

    def display_next_shape(self):
        if isinstance(self.game.next_shape, OShape) or isinstance(self.game.next_shape, IShape):
            self.draw_shape(self.game.next_shape, 412, 250)
        else:
            self.draw_shape(self.game.next_shape, 419, 250)

    def display_borders(self):
        o = OShape()
        self.draw_shape(o, 10, 50)
        self.draw_shape(o, 510, 450)
        i = IShape()
        self.draw_shape(i, 90, 70)
        self.draw_shape(i, 430, 470)
        j = JShape()
        self.draw_shape(j, 190, 50)
        self.draw_shape(j, 350, 450)
        l = LShape()
        self.draw_shape(l, 270, 50)
        self.draw_shape(l, 270, 450)
        s = SShape()
        self.draw_shape(s, 350, 50)
        self.draw_shape(s, 190, 450)
        z = ZShape()
        self.draw_shape(z, 430, 50)
        self.draw_shape(z, 110, 450)
        t = TShape()
        self.draw_shape(t, 510, 50)
        self.draw_shape(t, 30, 450)

    def display_game_over_text(self):
        game_text = large_text.render("GAME", True, "white")
        self.window.blit(game_text, (180 - (game_text.get_width() / 2), 200))
        over_text = large_text.render("OVER!", True, "white")
        self.window.blit(over_text, (180 - (over_text.get_width() / 2), 300))

    def update_high_score(self):
        if self.game.score > self.high_score:
            with open("high_score.txt", "w") as f:
                f.write(str(self.game.score))

    def display_restart_button(self):
        self.make_button(RESTART_X, RESTART_Y, "restart")

    def reset_game(self):
        self.game = None

        with open("high_score.txt") as f:
            self.high_score = int(f.read())

    def make_button(self, x_pos, y_pos, text):
        if x_pos < self.mouse_pos[0] < x_pos+BUTTON_WIDTH and y_pos < self.mouse_pos[1] < y_pos+BUTTON_HEIGHT:
            pygame.draw.rect(self.window, BUTTON_COLOR, (x_pos, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)
        else:
            pygame.draw.rect(self.window, BUTTON_HOVER, (x_pos, y_pos, BUTTON_WIDTH, BUTTON_HEIGHT), border_radius=10)

        button_text = medium_text.render(text, True, BUTTON_TEXT_COLOR)
        self.window.blit(button_text, (x_pos+(BUTTON_WIDTH/2)-(button_text.get_width()/2), y_pos+5))


Tetris()
