import pygame
from Ball import *
from Button import *
from Hole import *
from Purse import *
from Wall import *
pygame.init()


switch_menu = {"game": True, "start": False, "game_over": False}


class Game:
    def __init__(self, sc, size_menu):
        self.sc, self.size_menu = sc, size_menu
        self.size_field = [1200, 800]
        self.field_spawn_balls = [0, 50, 1199, 700]
        self.cord_field = [(self.size_menu[0] - self.size_field[0]) // 2, 0]
        self.field_surface = pygame.Surface(self.size_field)

        self.clock = pygame.time.Clock()
        self.FPS = 500

        self.number_balls = 20
        self.min_r, self.max_r = 30, 30
        self.mas_colors_ball = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 128), (200, 0, 200), (255, 51, 153),
                                (255, 153, 51), (0, 153, 0)]
        self.index_pressed_ball = -1
        self.price_ball = 1
        self.one_control_ball = True

        self.point_account = Purse(0)
        self.size_hole = 60

        mas_cord_button = [[15, 25], [15, 85]]
        mas_size_button = [[125, 50], [125, 50]]
        mas_text_button = ["comback start_menu", "respawn balls"]
        mas_function = [self.comback_start_menu, self.respawn_balls]
        self.mas_buttons = []
        for i in range(len(mas_function)):
            self.mas_buttons.append(Button(mas_cord_button[i], mas_text_button[i], mas_function[i], mas_size_button[i], 16))

        self.work_while = False

        self.respawn_balls()

        self.mas_walls = [Wall(self.size_hole, 50, 1199 // 2 - self.size_hole, 50),
                          Wall(self.size_hole + 1199 // 2, 50, 1199 - self.size_hole, 50),
                          Wall(0, 50 + self.size_hole, 0, 750 - self.size_hole),
                          Wall(1199, 50 + self.size_hole, 1199, 750 - self.size_hole),
                          Wall(0 + self.size_hole, 750, 1199 // 2 - self.size_hole, 750),
                          Wall(1199 // 2 + self.size_hole, 750, 1199 - self.size_hole, 750)]

        self.mas_holes = [Hole([0, 50], self.size_hole), Hole([self.size_field[0] // 2, 30], self.size_hole),
                          Hole([self.size_field[0], 50], self.size_hole), Hole([0, self.size_field[1] - 50], self.size_hole),
                          Hole([self.size_field[0] // 2, self.size_field[1] - 30], self.size_hole), Hole([self.size_field[0], self.size_field[1] - 50], self.size_hole)]

    def comback_start_menu(self):
        self.work_while = False
        change_menu("start")

    def respawn_balls(self):
        self.mas_balls = [Controls_ball(randint(self.max_r + self.field_spawn_balls[0], self.field_spawn_balls[2] - self.max_r),
                                        randint(self.max_r + self.field_spawn_balls[1], self.field_spawn_balls[3] - self.max_r),
                                        randint(self.min_r, self.max_r), self.FPS)]

        self.mas_balls.extend(
            [Ball(randint(self.max_r + self.field_spawn_balls[0], self.field_spawn_balls[2] - self.max_r),
                  randint(self.max_r + self.field_spawn_balls[1], self.field_spawn_balls[3] - self.max_r),
                  randint(self.min_r, self.max_r), self.FPS, i + 1, choice(self.mas_colors_ball)) for i in range(self.number_balls)])

    def collision_responce(self, ball1, ball2):
        distance = self.get_distance(ball1.x, ball2.x, ball1.y, ball2.y)

        if not distance:
            return

        normal_x, normal_y = (ball2.x - ball1.x) / distance, (ball2.y - ball1.y) / distance
        perpenducular_x, perpenducular_y = -normal_y, normal_x

        dpNorm1 = ball1.vx * normal_x + ball1.vy * normal_y
        dpNorm2 = ball2.vx * normal_x + ball2.vy * normal_y

        dpPerpend1 = ball1.vx * perpenducular_x + ball1.vy * perpenducular_y
        dpPerpend2 = ball2.vx * perpenducular_x + ball2.vy * perpenducular_y

        m1 = (dpNorm1 * (ball1.mass - ball2.mass) + 2 * ball2.mass * dpNorm2) / (ball1.mass + ball2.mass)
        m2 = (dpNorm2 * (ball2.mass - ball1.mass) + 2 * ball1.mass * dpNorm1) / (ball1.mass + ball2.mass)

        ball1.vx = perpenducular_x * dpPerpend1 + normal_x * m1
        ball1.xy = perpenducular_y * dpPerpend1 + normal_y * m1
        ball2.vx = perpenducular_x * dpPerpend2 + normal_x * m2
        ball2.vy = perpenducular_y * dpPerpend2 + normal_y * m2

        over_move = 0.5 * (distance - ball1.r - ball2.r)
        ball1.x -= over_move * (ball1.x - ball2.x) / distance
        ball1.y -= over_move * (ball1.y - ball2.y) / distance
        ball2.x += over_move * (ball1.x - ball2.x) / distance
        ball2.y += over_move * (ball1.y - ball2.y) / distance

    def check_touch_to_walls(self, ball):
        for wall in self.mas_walls:
            l = self.check_touch_circle_line(ball, wall)
            if not (l is False):
                q = (2 * (ball.vx * wall.normal_x + ball.vy * wall.normal_y)) / (wall.normal_x ** 2 + wall.normal_y ** 2)
                qn = [q * wall.normal_x, q * wall.normal_y]
                ball.vx, ball.vy = ball.vx - qn[0], ball.vy - qn[1]
                len_movment_vector = math.sqrt(ball.vx ** 2 + ball.vy ** 2)
                if not len_movment_vector:
                    return
                excessive_move_x, excessive_move_y = ball.vx * ((ball.r - l) / len_movment_vector), ball.vy * ((ball.r - l) / len_movment_vector)
                ball.x += excessive_move_x
                ball.y += excessive_move_y

    def check_touch_circle_line(self, circle, wall):
        x_crossing, y_crossing = wall.get_intersection_point_line(circle.x, circle.y)
        if self.get_distance(circle.x, x_crossing, circle.y, y_crossing) > circle.r:
            return False
        if wall.check_belong_wall(x_crossing, y_crossing):
            return self.get_distance(circle.x, x_crossing, circle.y, y_crossing)
        len_to_left_edge = self.get_distance(wall.x1, circle.x, wall.y1, circle.y)
        len_to_rigth_edge = self.get_distance(wall.x2, circle.x, wall.y2, circle.y)
        if len_to_left_edge <= circle.r:
            return len_to_left_edge
        if len_to_rigth_edge <= circle.r:
            return len_to_rigth_edge
        return False

    def key_mouse_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.mas_balls[0].check_in_point(*self.get_local_mouse_pos()):
                        self.index_pressed_ball = 0

                    for but in self.mas_buttons:
                        but.check_click_but(*pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.index_pressed_ball != -1:
                        self.mas_balls[0].vx = (self.mas_balls[0].x - self.get_local_mouse_pos()[0]) * 4
                        self.mas_balls[0].vy = (self.mas_balls[0].y - self.get_local_mouse_pos()[1]) * 4
                        self.index_pressed_ball = -1

    def output_balls(self, sc):
        for i, ball in enumerate(self.mas_balls):
            self.check_touch_to_walls(ball)
            ball.update()
            pygame.draw.circle(sc, ball.color, (ball.x, ball.y), ball.r)
            ball.blit_text(self.field_surface)

    def react_ball_hole(self, circle1, circle2):
        if circle2.r < circle1.r:
            return
        if math.ceil(circle2.r / 5) >= self.get_distance(circle2.x, circle1.x, circle2.y, circle1.y):
            self.remove_ball(circle1)
            return
        if circle2.r >= self.get_distance(circle2.x, circle1.x, circle2.y, circle1.y):
            circle1.vx, circle1.vy = (circle2.x - circle1.x) * 5, (circle2.y - circle1.y) * 5

    def reaction_collision(self, circle1, circle2):
        if (type(circle1) == Ball or type(circle1) == Controls_ball) and \
                (type(circle2) == Ball or type(circle2) == Controls_ball):
            if circle1.r + circle2.r >= self.get_distance(circle2.x, circle1.x, circle2.y, circle1.y):
                self.collision_responce(circle1, circle2)
        elif (type(circle1) == Ball or type(circle1) == Controls_ball) and type(circle2) == Hole:
            self.react_ball_hole(circle1, circle2)
        elif (type(circle2) == Ball or type(circle2) == Controls_ball) and type(circle1) == Hole:
            self.react_ball_hole(circle2, circle1)

    def check_collision(self):
        mas_couple = []
        mas_edge_circles = sorted([[c.x - c.r, c.x + c.r, c] for c in self.mas_balls + self.mas_holes],
                                  key=lambda x: x[0])
        i = 0
        while i < len(mas_edge_circles):
            a = i + 1
            while a != len(mas_edge_circles) and mas_edge_circles[i][1] >= mas_edge_circles[a][0]:
                mas_couple.append([i, a])
                a += 1
            i += 1

        for couple in mas_couple:
            circle1, circle2 = mas_edge_circles[couple[0]][2], mas_edge_circles[couple[1]][2]
            if (type(circle1) == Ball or type(circle1) == Controls_ball) and \
                    (type(circle2) == Ball or type(circle2) == Controls_ball):
                if circle1.r + circle2.r >= self.get_distance(circle2.x, circle1.x, circle2.y, circle1.y):
                    self.collision_responce(circle1, circle2)
            elif (type(circle1) == Ball or type(circle1) == Controls_ball) and type(circle2) == Hole:
                self.react_ball_hole(circle1, circle2)
            elif (type(circle2) == Ball or type(circle2) == Controls_ball) and type(circle1) == Hole:
                self.react_ball_hole(circle2, circle1)

    def remove_ball(self, circle):
        for i, ball in enumerate(self.mas_balls):
            if circle.index_item == ball.index_item:
                self.mas_balls.pop(i)
                break

        self.point_account.increase_number(self.price_ball)
        if type(circle) == Controls_ball and self.one_control_ball:
            self.mas_balls.insert(0, Controls_ball(self.size_field[0] // 2, self.size_field[1] // 2, circle.r, circle.FPS))
            self.point_account.digrease_number(self.price_ball * 2)

    def get_distance(self, x1, x2, y1, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_local_mouse_pos(self):
        pos = pygame.mouse.get_pos()
        return [int(pos[0] - self.cord_field[0]), int(pos[1] - self.cord_field[1])]

    def main(self):
        self.work_while = True
        while self.work_while:
            self.key_mouse_event()
            self.sc.fill((255, 255, 255))
            self.sc.blit(self.field_surface, self.cord_field)
            self.field_surface.fill((200, 200, 200))
            for i in self.mas_holes:
                pygame.draw.circle(self.field_surface, (0, 200, 200), [i.x, i.y], i.r)
            self.check_collision()
            self.output_balls(self.field_surface)

            if self.index_pressed_ball != -1:
                pygame.draw.line(self.field_surface, (0, 255, 0),
                        [self.mas_balls[self.index_pressed_ball].x, self.mas_balls[self.index_pressed_ball].y], self.get_local_mouse_pos(), 3)

            for wall in self.mas_walls:
                pygame.draw.line(self.field_surface, (0, 0, 0), [wall.x1, wall.y1], [wall.x2, wall.y2], 1)

            for but in self.mas_buttons:
                but.blit_surface(self.sc)

            pygame.display.update()
            self.clock.tick(self.FPS)

class Start_menu:
    def __init__(self, sc, size_main_surface):
        self.sc, self.size_main_surface = sc, size_main_surface
        self.clock = pygame.time.Clock()
        self.FPS = 60
        mas_cord_button = [[100, 100], [100, 600]]
        mas_size_button = [[200, 100], [200, 100]]
        mas_text_button = ["Start game", "Exit"]
        mas_function = [self.start_game, self.quit]
        self.mas_buttons = []
        self.work_while = False
        for i in range(len(mas_function)):
            self.mas_buttons.append(Button(mas_cord_button[i], mas_text_button[i], mas_function[i], mas_size_button[i]))

    def start_game(self):
        self.work_while = False
        change_menu("game")

    def quit(self):
        exit()

    def main(self):
        self.work_while = True
        while self.work_while:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for but in self.mas_buttons:
                        but.check_click_but(*pygame.mouse.get_pos())
            self.sc.fill((255, 255, 255))
            for but in self.mas_buttons:
                but.blit_surface(self.sc)

            pygame.display.update()
            self.clock.tick(self.FPS)

def change_menu(menu):
    for i in switch_menu:
        switch_menu[i] = False
    switch_menu[menu] = True

if __name__ == "__main__":
    size_menu = [1500, 800]
    sc = pygame.display.set_mode(size_menu)
    game = Game(sc, size_menu)
    start_menu_field = Start_menu(sc, size_menu)
    while True:
        if switch_menu["game"]:
            game.main()
        if switch_menu["start"]:
            start_menu_field.main()
        if switch_menu["game_over"]:
            pass
