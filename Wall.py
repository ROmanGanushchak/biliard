import math


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.normal_x, self.normal_y = -(y2 - y1), x2 - x1
    
    def check_belong_wall(self, x, y):
        if (self.x1 <= x <= self.x2 or self.x2 <= x <= self.x1) and (self.y1 <= y <= self.y2 or self.y1 >= y >= self.y2):
            return True
        return

    def get_intersection_point_line(self, x, y):
        if self.x1 == self.x2:
           return [self.x1, y]
        if self.y1 == self.y2:
            return [x, self.y1]
        k = (self.y2 - self.y1) / (self.x2 - self.x1)
        p = self.y1 - k * self.x1
        k_perpend = -1 / k
        p_perpend = y - k * x
        x_crossing = (p_perpend - p) / (k - k_perpend)
        y_crossing = k * x_crossing + p
        return [x_crossing, y_crossing]

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)