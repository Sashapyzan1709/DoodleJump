import pygame
from src.sprite import Sprite

class Monster(Sprite):
    def __init__(self, center: list[float], image: pygame.Surface, health: int, speed: float,):
        super().__init__(center, image)
        self.health = health
        self.speed = speed
        self.stats_pos = center
        self.offset_y = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= self.stats_pos[1] + self.offset_y:
            self.speed = -abs(self.speed)
        if self.rect.y <= self.stats_pos[1] - self.offset_y:
            self.speed = abs(self.speed)


