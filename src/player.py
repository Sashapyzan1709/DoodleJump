import pygame
from src.config import WIN_WIDTH, GRAVITY, JUMP_POWER
from src.sprite import Sprite

class Player(Sprite):
    def __init__(self, center : list[float], image : pygame.surface, speed : float, jump_sound: pygame.Sound,):
        super().__init__(center, image)
        self.origin_image = image.copy()
        self.speed = speed
        self.valocity_y = 0
        self.jump_sound = jump_sound

    def update(self, platforms : list[Sprite]):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.image = self.origin_image.copy()
            self.rect.x -= self.speed
            if self.rect.right <= 0:
                self.rect.left = WIN_WIDTH
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.image = pygame.transform.flip(self.origin_image, True, False)
            self.rect.x += self.speed
            if self.rect.left >= WIN_WIDTH:
                self.rect.right = 0
        
        self.valocity_y = min(self.valocity_y + GRAVITY, 15)
        self.rect.y += self.valocity_y
        for platform in platforms:
            if platform.rect.colliderect(self.rect) and self.valocity_y > 0 and platform.rect.bottom >= self.rect.bottom:
                self.valocity_y = -JUMP_POWER
                self.rect.bottom = platform.rect.top
                platform.on_collide(self)
                if pygame.mixer.get_init():
                    self.jump_sound.play()
                    