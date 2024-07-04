import math

class Hole:
    def __init__(self, pos, r, texture=False):
        self.x, self.y = pos[0], pos[1]
        self.r, self.texture = r, texture

    def get_distance(self, pos):
        return math.sqrt((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2)

    def check_belong(self, pos):
        if self.get_distance(pos) < self.r:
            return True
        return False

    def get_vector_inside(self, pos):
        return [self.x - pos[0], self.y - pos[1]]

    def get_edge_points(self):
        return [[self.x + self.r, self.y],
                [self.x, self.y + self.r],
                [self.x - self.r, self.y],
                [self.x, self.y - self.r]]