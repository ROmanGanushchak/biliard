import pygame
pygame.init()

class Button:
    def __init__(self, pos, text, function, size, size_text=30):
        self.x, self.y, self.size_x, self.size_y = pos[0], pos[1], size[0], size[1]
        self.function = function
        f = pygame.font.Font(None, size_text)
        self.text = f.render(text, True, (255, 255, 255))
        self.surfaace = self.creat_surface_button()

    def check_click_but(self, cord_mouse_x, cord_mouse_y):
        if self.x <= cord_mouse_x <= self.x + self.size_x and self.y <= cord_mouse_y <= self.y + self.size_y:
            self.function()

    def creat_surface_button(self):
        surfce_button = pygame.Surface((self.size_x, self.size_y))
        surfce_button.fill((100, 100, 100))
        place = self.text.get_rect(center=(self.size_x // 2, self.size_y // 2))
        surfce_button.blit(self.text, place)
        return surfce_button

    def blit_surface(self, sc):
        sc.blit(self.surfaace, [self.x, self.y])

