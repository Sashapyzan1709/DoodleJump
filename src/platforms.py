from random import randint

import pygame

from src.config import (
    DESTROY_PLATFORM,
    PLATFROM_SPEED_MAX,
    PLATFROM_SPEED_MIN,
    WIN_WIDTH,
)
from src.sprite import Sprite


class Platform(Sprite):
    def on_collide(self, player: Sprite):
        pass

    def update(self):
        pass


class MovingPlatform(Platform):
    def __init__(self, center: list[float], image: pygame.Surface):
        super().__init__(center, image)
        self.speed = randint(PLATFROM_SPEED_MIN, PLATFROM_SPEED_MAX)

    def update(self):
        if self.rect.right >= WIN_WIDTH:
            self.speed = -abs(self.speed)
        if self.rect.left <= 0:
            self.speed = abs(self.speed)

        self.rect.x += self.speed


class TrapPlatform(Platform):
    def on_collide(self, player: Sprite):
        event = pygame.Event(DESTROY_PLATFORM, platform=self)
        pygame.event.post(event)


class BatutPlatform(Platform):
    def on_collide(self, player: Sprite):
        player.valocity_y *= 1.5