from random import randint

import pygame

from src.sprite import Sprite
from src.player import Player
from src.config import WIN_HEIGHT, WIN_SIZE, WIN_WIGHT, SPAWN_STEP

def main():  
    window = pygame.Window("Doodle Jump", WIN_SIZE)
    surface = window.get_surface()

    platform_image = pygame.image.load("asset/platform.png")
    platforms = [Sprite([200, 550],platform_image)]
    for y in range(550 - SPAWN_STEP, 0, -SPAWN_STEP):
        platforms.append(Sprite([randint(0, WIN_WIGHT), y],platform_image))

    
    player_image = pygame.image.load("asset/player.png")
    player = Player([200, 450], player_image, 6)
    window.set_icon(player_image)

    background_image = pygame.image.load("asset/background.png")
    background_image = pygame.transform.scale(background_image, WIN_SIZE)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                running = False
        clock.tick(60)
        player.update(platforms)

        surface.blit(background_image)
        for platform in platforms:
            platform.render(surface)
        player.render(surface)

        window.flip()

if __name__ == "__main__":
    main()